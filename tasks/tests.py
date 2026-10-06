import json
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import Client, TestCase, override_settings
from .models import Task

class EndpointTests(TestCase):
    def test_health(self):
        r = self.client.get('/health/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'status': 'ok'})

    def test_home_and_about(self):
        for url in ['/', '/about/']:
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json()['project'], 'Task Manager')

    @override_settings(TASKS_USE_DB=False)
    def test_python_list_stage(self):
        self.assertEqual(len(self.client.get('/tasks/').json()), 3)
        self.assertEqual(self.client.get('/tasks/1/').json()['id'], 1)
        self.assertEqual(self.client.get('/tasks/999/').status_code, 404)

    def test_database_stage(self):
        task = Task.objects.create(title='ORM task')
        self.assertEqual(self.client.get(f'/tasks/{task.pk}/').json()['title'], 'ORM task')
        self.assertEqual(len(self.client.get('/tasks/').json()), 1)

    def test_missing_task_json(self):
        r = self.client.get('/tasks/999/')
        self.assertEqual(r.status_code, 404)
        self.assertIn('error', r.json())

    def test_echo_all_json_values(self):
        for value in [{'title': 'Қазақша'}, [1, 2], 'text', 4, True, None]:
            r = self.client.post('/echo/', json.dumps(value), content_type='application/json')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.json(), value)

    def test_echo_invalid_json(self):
        for value in [b'{bad}', b'\xff', b'', b'NaN']:
            r = self.client.post('/echo/', value, content_type='application/json')
            self.assertEqual(r.status_code, 400)
            self.assertIn('error', r.json())

    def test_http_methods(self):
        self.assertEqual(self.client.get('/echo/').status_code, 405)
        self.assertEqual(self.client.post('/health/').status_code, 405)

    def test_csrf_is_only_exempt_for_echo(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post('/echo/', '{}', content_type='application/json').status_code, 200)
        self.assertEqual(client.post('/admin/login/', {}).status_code, 403)

class ModelTests(TestCase):
    def test_crud_filter_order(self):
        a = Task.objects.create(title='First')
        b = Task.objects.create(title='Second', status=Task.Status.DONE)
        self.assertEqual(Task.objects.filter(status='done').count(), 1)
        self.assertEqual(list(Task.objects.order_by('created_at', 'id').values_list('id', flat=True)), [a.pk, b.pk])
        a.status = Task.Status.IN_PROGRESS
        a.save()
        a.refresh_from_db()
        self.assertEqual(a.status, 'in_progress')
        b.delete()
        self.assertEqual(Task.objects.count(), 1)

    def test_status_validation(self):
        with self.assertRaises(ValidationError):
            Task(title='Invalid', status='wrong').full_clean()
        with self.assertRaises(IntegrityError), transaction.atomic():
            Task.objects.create(title='Invalid', status='wrong')

class AdminTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser('tester', 'tester@example.com', 'Test-only-Password-584!')
        self.client.force_login(self.user)

    def test_requires_login(self):
        self.assertEqual(Client().get('/admin/tasks/task/').status_code, 302)

    def test_admin_columns_search_and_filter(self):
        task = Task.objects.create(title='Unique needle', status='done')
        Task.objects.create(title='Other', status='todo')
        r = self.client.get('/admin/tasks/task/', {'q': 'needle', 'status__exact': 'done'})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(list(r.context['cl'].result_list), [task])
        self.assertEqual(r.context['cl'].list_display, ['action_checkbox', 'title', 'status', 'created_at'])

    def test_admin_crud_with_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        client.get('/admin/tasks/task/add/')
        token = client.cookies['csrftoken'].value
        r = client.post('/admin/tasks/task/add/', {'csrfmiddlewaretoken': token,
            'title': 'Admin created', 'description': 'HTTP form', 'status': 'todo', '_save': '1'})
        self.assertEqual(r.status_code, 302)
        task = Task.objects.get(title='Admin created')
        r = client.post(f'/admin/tasks/task/{task.pk}/change/', {'csrfmiddlewaretoken': token,
            'title': 'Admin updated', 'description': 'HTTP form', 'status': 'done', '_save': '1'})
        self.assertEqual(r.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Admin updated')
        r = client.post(f'/admin/tasks/task/{task.pk}/delete/', {'csrfmiddlewaretoken': token, 'post': 'yes'})
        self.assertEqual(r.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
