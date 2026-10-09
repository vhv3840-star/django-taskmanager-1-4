import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Task


# Екінші жұмыста деректер осы тізімде сақталады.
DEMO_TASKS = [
    {"id": 1, "title": "Django жобасын құру", "status": "done"},
    {"id": 2, "title": "URL маршруттарын қосу", "status": "in_progress"},
    {"id": 3, "title": "Task моделін жасау", "status": "todo"},
]


@require_GET
def health(request):
    return JsonResponse({"status": "ok"})


@require_GET
def home(request):
    return JsonResponse({
        "project": "Task Manager",
        "message": "Қош келдіңіз!",
    }, json_dumps_params={"ensure_ascii": False})


@require_GET
def about(request):
    return JsonResponse({
        "project": "Task Manager",
        "author": "Джанкилиш Ерсайн",
        "module": "Django негіздері",
    }, json_dumps_params={"ensure_ascii": False})


# Дерекқордағы объектіні JSON үшін сөздікке айналдырамыз.
def task_to_dict(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "created_at": task.created_at.isoformat(),
    }


@require_GET
def task_list(request):
    if settings.TASKS_USE_DB:
        tasks = []
        for task in Task.objects.all():
            tasks.append(task_to_dict(task))
    else:
        tasks = DEMO_TASKS

    return JsonResponse(tasks, safe=False,
                        json_dumps_params={"ensure_ascii": False})


@require_GET
def task_detail(request, id):
    if settings.TASKS_USE_DB:
        try:
            task = Task.objects.get(id=id)
        except Task.DoesNotExist:
            return JsonResponse({"error": "Тапсырма табылмады"}, status=404,
                                json_dumps_params={"ensure_ascii": False})
        return JsonResponse(task_to_dict(task),
                            json_dumps_params={"ensure_ascii": False})

    for task in DEMO_TASKS:
        if task["id"] == id:
            return JsonResponse(task, json_dumps_params={"ensure_ascii": False})

    return JsonResponse({"error": "Тапсырма табылмады"}, status=404,
                        json_dumps_params={"ensure_ascii": False})


# NaN және Infinity JSON форматында қолданылмайды.
def reject_constant(value):
    raise ValueError("JSON мәні қате: " + value)


# CSRF тек осы оқу маршруты үшін өшірілген.
@csrf_exempt
@require_POST
def echo(request):
    try:
        text = request.body.decode("utf-8")
        data = json.loads(text, parse_constant=reject_constant)
    except (UnicodeDecodeError, ValueError):
        return JsonResponse({"error": "JSON пішімі қате"}, status=400,
                            json_dumps_params={"ensure_ascii": False})

    return JsonResponse(data, safe=False,
                        json_dumps_params={"ensure_ascii": False})
