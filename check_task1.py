"""Verify practical work 1 against the running Django server."""
import os
import sys
import urllib.request
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskmanager.settings")
django.setup()
print("Python:", sys.version.split()[0])
print("Django:", django.get_version())
print("Virtual environment:", sys.prefix != sys.base_prefix)
call_command("check")
url = "http://127.0.0.1:8000/health/"
with urllib.request.urlopen(url) as response:
    print("GET", url)
    print("HTTP", response.status)
    print("Content-Type:", response.headers["Content-Type"])
    print("Response:", response.read().decode())
