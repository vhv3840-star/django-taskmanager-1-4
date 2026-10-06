from tasks.models import Task

print('PRACTICAL WORK 3 - DJANGO SHELL AND ORM')
if Task.objects.exists():
    raise RuntimeError('Use an empty demo Task table; existing data is preserved.')
titles = ['Django жобасын құру', 'URL маршруттарын қосу', 'Task моделін жасау',
          'Миграцияларды қолдану', 'Admin панелін баптау']
for i, title in enumerate(titles):
    Task.objects.create(title=title, description='Практикалық жұмыс',
                        status=['todo', 'in_progress', 'done', 'todo', 'todo'][i])
print('CREATE - Task.objects.count():', Task.objects.count())
for task in Task.objects.order_by('id'):
    print(task.pk, task.title, task.status)
print('FILTER todo:', list(Task.objects.filter(status='todo').values_list('id', flat=True)))
print('ORDER created_at:', list(Task.objects.order_by('created_at').values_list('id', flat=True)))
first = Task.objects.order_by('id').first()
first.status = 'done'
first.save()
first.refresh_from_db()
print('UPDATE:', first.pk, first.status)
last = Task.objects.order_by('id').last()
deleted_id = last.pk
last.delete()
print('DELETE:', deleted_id, 'exists:', Task.objects.filter(pk=deleted_id).exists())
print('FINAL COUNT:', Task.objects.count())
