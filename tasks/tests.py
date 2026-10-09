import json
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import Client, TestCase, override_settings
from django.conf import settings
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
        self.assertIn('django.middleware.csrf.CsrfViewMiddleware', settings.MIDDLEWARE)
        self.assertEqual(client.post('/health/', {}).status_code, 403)

    def test_admin_removed(self):
        self.assertEqual(self.client.get('/admin/').status_code, 404)
        self.assertNotIn('django.contrib.admin', settings.INSTALLED_APPS)

class ModelTests(TestCase):
    def test_crud_filter_order(self):
        a = Task.objects.create(title='First')
        b = Task.objects.create(title='Second', status='done')
        self.assertEqual(Task.objects.filter(status='done').count(), 1)
        self.assertEqual(list(Task.objects.order_by('created_at', 'id').values_list('id', flat=True)), [a.pk, b.pk])
        a.status = 'in_progress'
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
