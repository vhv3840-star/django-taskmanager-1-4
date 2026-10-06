import os
import sys
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
django.setup()
print('PRACTICAL WORK 1 - DJANGO PROJECT')
print('Python:', sys.version.split()[0])
print('Django:', django.get_version())
print('Virtual environment:', sys.prefix != sys.base_prefix)
print('Application: tasks.apps.TasksConfig')
call_command('check')
