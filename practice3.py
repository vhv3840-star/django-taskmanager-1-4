
import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')
django.setup()
call_command('makemigrations', 'tasks')
call_command('migrate')
call_command('shell', command="exec(open('orm_demo.py', encoding='utf-8').read())")
