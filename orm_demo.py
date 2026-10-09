from tasks.models import Task

# Бұл мысалды бос Task кестесінде орындаймыз.
if Task.objects.exists():
    raise RuntimeError("Task кестесі бос емес. ORM мысалы үшін бөлек бос база қолданыңыз.")

Task.objects.create(title="Django жобасын құру", description="Жобаны дайындау", status="done")
Task.objects.create(title="Маршруттарды қосу", description="GET сұраныстары", status="in_progress")
Task.objects.create(title="Task моделін жасау", description="Модель өрістері", status="todo")
Task.objects.create(title="Миграция жасау", description="SQLite кестесін құру", status="todo")
Task.objects.create(title="Есепті дайындау", description="Жұмысты қорғау", status="todo")

print("Барлық тапсырмалар:")
for task in Task.objects.all():
    print(task.id, task.title, task.status)

print("Орындалмаған тапсырмалар:")
for task in Task.objects.filter(status="todo"):
    print(task.id, task.title)

print("Уақыт бойынша сұрыптау:")
for task in Task.objects.order_by("created_at"):
    print(task.id, task.title, task.created_at)

# Бірінші жазбаны өзгертеміз, басқа жазбаны өшіреміз.
first = Task.objects.order_by("id").first()
first.status = "in_progress"
first.save()
print("Өзгертілді:", first.id, first.status)

last = Task.objects.order_by("id").last()
deleted_id = last.id
last.delete()
print("Өшірілді:", deleted_id)
print("Қалған тапсырмалар саны:", Task.objects.count())
