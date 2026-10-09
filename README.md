# Task Manager — 1–3 практикалық жұмыс

Автор: Джанкилиш Ерсайн. Django 5.2.17, Python 3.10 немесе жаңасы, SQLite.

## PyCharm арқылы іске қосу

Архивті ашып, taskmanager қалтасын PyCharm бағдарламасында ашыңыз.
Терминалда келесі командаларды ретімен орындаңыз:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Егер ортаны белсендіру командасы орындалмаса, оның Python файлын тікелей қолданыңыз:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Серверді тоқтату: Ctrl+C. Сервер жұмыс істеп тұрғанда басқа командаларға екінші терминал ашыңыз.

## 1-жұмыс

tasks қосымшасы settings.py ішіндегі INSTALLED_APPS тізіміне қосылған.
/health/ адресі сервердің жауап беретінін тексереді.

```powershell
python manage.py check
```

Браузерде http://127.0.0.1:8000/health/ ашыңыз. Жауап: {"status": "ok"}.

## 2-жұмыс

Бұл кезеңде тапсырмалар Python тізімінен алынады.
Серверді тоқтатып, тізім режимін қосыңыз:

```powershell
$env:TASKS_USE_DB = '0'
python manage.py runserver
```

Браузерде ретімен ашыңыз:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/about/
- http://127.0.0.1:8000/tasks/
- http://127.0.0.1:8000/tasks/1/
- http://127.0.0.1:8000/tasks/999/

Алғашқы төрт адрес 200 жауабын қайтарады. Соңғы адрес жоқ тапсырмаға арналған, сондықтан 404 береді.

Екінші PowerShell терминалында POST сұранысын тексеріңіз:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/echo/" -Method Post -ContentType "application/json" -Body '{"message":"Hello Django"}'
```

/echo/ келген JSON мәнін қайтарады. Қате JSON үшін 400, GET үшін 405 жауабы келеді.
CSRF тек echo функциясында өшірілген; жалпы middleware сақталған.

## 3-жұмыс

Task моделінің өрістері: title, description, status және created_at.
status мәндері: todo, in_progress және done.
Серверді тоқтатып, дерекқор режимін қосыңыз:

```powershell
$env:TASKS_USE_DB = '1'
python manage.py makemigrations tasks
python manage.py migrate
python manage.py shell
```

Shell ішінде ORM мысалын орындаңыз:

```python
exec(open('orm_demo.py', encoding='utf-8').read())
```

Мысал бес жазба қосады, барлық жазбаны оқиды, күйі бойынша сүзеді және уақыт бойынша сұрыптайды.
Бірінші жазбаны өзгертеді, соңғы жазбаны өшіреді. Соңында төрт тапсырма қалады.
Мысал бос Task кестесінде орындалады. Кестеде бұрынғы жазбалар болса, оларды өзгертпей тоқтайды.
Shell бағдарламасынан шығу: exit().


## Файлдардың қызметі

- manage.py — Django командаларын орындау.
- taskmanager/settings.py — жоба баптаулары.
- taskmanager/urls.py — tasks маршруттарын қосу.
- tasks/urls.py — адрес пен функцияны байланыстыру.
- tasks/views.py — сұранысты өңдеу және JSON жауап беру.
- tasks/models.py — тапсырма моделі.
- tasks/migrations/ — дерекқор кестесінің құрылымы.
- orm_demo.py — үшінші жұмыстың ORM мысалы.
- tasks/tests.py — маршруттар мен модельді тексеру.

## Тексеру

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test tasks
```
