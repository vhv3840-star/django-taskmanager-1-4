"""Run with: python manage.py shell -c \"exec(open('demo_shell.py', encoding='utf-8').read())\"."""
import json
import os
import secrets
from pathlib import Path
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import Client, override_settings
from django.test.utils import setup_test_environment
from tasks.models import Task

setup_test_environment()
print('=== Practical work 3: Django Shell and ORM ===')
if Task.objects.exists():
    raise RuntimeError('Demo requires an empty tasks table to avoid changing existing data.')
titles = ['Django жобасын құру', 'URL маршруттарын қосу', 'Task моделін жасау',
          'Миграцияларды қолдану', 'Admin панелін баптау']
for i, title in enumerate(titles):
    Task.objects.create(title=title, description='Практикалық жұмыс', status=['todo', 'in_progress', 'done', 'todo', 'todo'][i])
print('Task.objects.count() ->', Task.objects.count())
print('Task.objects.filter(status="todo").count() ->', Task.objects.filter(status='todo').count())
ordered = list(Task.objects.order_by('created_at', 'id').values_list('id', flat=True))
print('Task.objects.order_by("created_at", "id") ->', ordered)
first = Task.objects.order_by('id').first()
first.status = 'done'
first.save()
first.refresh_from_db()
print(f'Task {first.pk} saved status ->', first.status)
last = Task.objects.order_by('id').last()
deleted_id = last.pk
last.delete()
print(f'Task {deleted_id} exists after delete ->', Task.objects.filter(pk=deleted_id).exists())
print('Final ORM count ->', Task.objects.count())

print('\n=== Practical works 1 and 2: HTTP requests ===')
client = Client(enforce_csrf_checks=True)
records = []
def record(method, url, response):
    data = response.json()
    records.append({'method': method, 'url': url, 'status': response.status_code, 'body': data})
    print(method, url, '->', response.status_code, json.dumps(data, ensure_ascii=False))
for url in ['/health/', '/', '/about/', '/tasks/', f'/tasks/{first.pk}/', '/tasks/999/']:
    record('GET', url, client.get(url))
record('POST', '/echo/', client.post('/echo/', json.dumps({'message': 'Сәлем Django', 'number': 4}), content_type='application/json'))
record('POST', '/echo/', client.post('/echo/', '{bad}', content_type='application/json'))
with override_settings(TASKS_USE_DB=False):
    record('GET', '/tasks/ [Python list]', client.get('/tasks/'))

print('\n=== Practical work 4: authenticated Admin HTTP forms ===')
username = 'demo_admin'
os.environ['DJANGO_SUPERUSER_PASSWORD'] = secrets.token_urlsafe(24)
if not get_user_model().objects.filter(username=username).exists():
    call_command('createsuperuser', username=username, email='demo@example.com', interactive=False)
os.environ.pop('DJANGO_SUPERUSER_PASSWORD', None)
admin_user = get_user_model().objects.get(username=username)
print('createsuperuser --noinput -> is_superuser:', admin_user.is_superuser)
print('Anonymous GET /admin/tasks/task/ ->', client.get('/admin/tasks/task/').status_code)
client.force_login(admin_user)
response = client.get('/admin/tasks/task/')
print('Authenticated GET /admin/tasks/task/ ->', response.status_code)
assert response.status_code == 200
client.get('/admin/tasks/task/add/')
token = client.cookies['csrftoken'].value
response = client.post('/admin/tasks/task/add/', {'csrfmiddlewaretoken': token,
    'title': 'Admin тексеру', 'description': 'HTTP форма арқылы қосылды', 'status': 'todo', '_save': '1'})
task = Task.objects.get(title='Admin тексеру')
print('POST Admin add ->', response.status_code, 'created id:', task.pk)
assert response.status_code == 302
response = client.post(f'/admin/tasks/task/{task.pk}/change/', {'csrfmiddlewaretoken': token,
    'title': 'Admin тексеру жаңартылды', 'description': 'Өзгертілді', 'status': 'done', '_save': '1'})
task.refresh_from_db()
print('POST Admin change ->', response.status_code, 'saved status:', task.status)
assert response.status_code == 302 and task.status == 'done'
response = client.get('/admin/tasks/task/', {'q': 'жаңартылды', 'status__exact': 'done'})
matches = list(response.context['cl'].result_list.values_list('title', flat=True))
print('GET Admin search and status filter ->', response.status_code, matches)
assert matches == ['Admin тексеру жаңартылды']
response = client.post(f'/admin/tasks/task/{task.pk}/delete/', {'csrfmiddlewaretoken': token, 'post': 'yes'})
print('POST Admin delete ->', response.status_code, 'exists:', Task.objects.filter(pk=task.pk).exists())
assert response.status_code == 302 and not Task.objects.filter(pk=task.pk).exists()
client.logout()
print('POST Admin login without CSRF ->', Client(enforce_csrf_checks=True).post('/admin/login/', {}).status_code)
Path('evidence').mkdir(exist_ok=True)
Path('evidence/http-results.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
