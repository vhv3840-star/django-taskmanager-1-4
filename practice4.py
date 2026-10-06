import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
django.setup()
from django.contrib.auth import get_user_model
from django.test import Client
from django.test.utils import setup_test_environment
from tasks.models import Task

setup_test_environment()
client = Client(enforce_csrf_checks=True)
user = get_user_model().objects.get(username='screenshot_admin')
print('PRACTICAL WORK 4 - DJANGO ADMIN HTTP FORMS')
print('Superuser:', user.username, 'is_superuser:', user.is_superuser)
print('Anonymous Admin:', client.get('/admin/tasks/task/').status_code)
client.force_login(user)
print('Authenticated Admin:', client.get('/admin/tasks/task/').status_code)
client.get('/admin/tasks/task/add/')
token = client.cookies['csrftoken'].value
response = client.post('/admin/tasks/task/add/', {'csrfmiddlewaretoken': token,
    'title': 'Admin тексеру', 'description': 'Admin HTTP форма арқылы қосылды',
    'status': 'todo', '_save': '1'})
task = Task.objects.get(title='Admin тексеру')
print('ADD FORM:', response.status_code, 'id:', task.pk)
response = client.post(f'/admin/tasks/task/{task.pk}/change/', {'csrfmiddlewaretoken': token,
    'title': 'Admin тексеру жаңартылды', 'description': 'Өзгертілді',
    'status': 'done', '_save': '1'})
task.refresh_from_db()
print('CHANGE FORM:', response.status_code, 'saved:', task.title, task.status)
response = client.get('/admin/tasks/task/', {'q': 'жаңартылды', 'status__exact': 'done'})
print('SEARCH + STATUS FILTER:', response.status_code,
      list(response.context['cl'].result_list.values_list('title', flat=True)))
response = client.post(f'/admin/tasks/task/{task.pk}/delete/',
                       {'csrfmiddlewaretoken': token, 'post': 'yes'})
print('DELETE FORM:', response.status_code, 'exists:', Task.objects.filter(pk=task.pk).exists())
print('Admin login without CSRF:', Client(enforce_csrf_checks=True).post('/admin/login/', {}).status_code)
