import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from .models import Task

DEMO_TASKS = [
    {'id': 1, 'title': 'Django жобасын құру', 'status': 'done'},
    {'id': 2, 'title': 'URL маршруттарын қосу', 'status': 'in_progress'},
    {'id': 3, 'title': 'Task моделін жасау', 'status': 'todo'},
]

def json_response(data, **kwargs):
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, **kwargs)

@require_GET
def health(request):
    return json_response({'status': 'ok'})

@require_GET
def home(request):
    return json_response({'project': 'Task Manager', 'message': 'Қош келдіңіз!'})

@require_GET
def about(request):
    return json_response({'project': 'Task Manager', 'author': 'Джанкилиш Ерсайн', 'module': 'Django негіздері'})

def serialize_task(task):
    return {'id': task.pk, 'title': task.title, 'description': task.description,
            'status': task.status, 'created_at': task.created_at.isoformat()}

@require_GET
def task_list(request):
    data = ([serialize_task(task) for task in Task.objects.all()]
            if settings.TASKS_USE_DB else DEMO_TASKS)
    return json_response(data)

@require_GET
def task_detail(request, id):
    if settings.TASKS_USE_DB:
        task = Task.objects.filter(pk=id).first()
        data = serialize_task(task) if task else None
    else:
        data = next((task for task in DEMO_TASKS if task['id'] == id), None)
    if data is None:
        return json_response({'error': 'Тапсырма табылмады'}, status=404)
    return json_response(data)

def reject_constant(value):
    raise ValueError(f'Invalid JSON constant: {value}')

# Only the learning echo endpoint is exempt; Admin keeps CSRF protection.
@csrf_exempt
@require_POST
def echo(request):
    try:
        data = json.loads(request.body.decode('utf-8'), parse_constant=reject_constant)
    except (UnicodeDecodeError, ValueError):
        return json_response({'error': 'JSON пішімі қате'}, status=400)
    return json_response(data)
