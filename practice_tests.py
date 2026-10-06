import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
django.setup()
call_command('check')
call_command('makemigrations', check=True, dry_run=True)
call_command('test', 'tasks', verbosity=1)
