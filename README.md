# Task Manager — Django практикалық жұмыстар 1–4

Автор: Джанкилиш Ерсайн. Python 3.10 немесе жаңасы, Django 5.2.17, SQLite.

## Орнату және іске қосу

PowerShell терминалында жоба қалтасына өтіп орындаңыз:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

PowerShell орта белсендіруді бұғаттаса, саясатты өзгертпей `.\.venv\Scripts\python.exe` арқылы командаларды орындауға болады.
`http://127.0.0.1:8000/health/` және `http://127.0.0.1:8000/admin/` беттерін ашыңыз.
Admin үшін өзіңіз жасаған суперпайдаланушы логині мен құпиясөзін қолданыңыз.

## Жұмыстар бойынша файлдар

- №1: `taskmanager/settings.py`, `tasks/apps.py`, `/health/`.
- №2: `tasks/urls.py`, `tasks/views.py`, GET/POST және JSON қателері.
- №3: `tasks/models.py`, `tasks/migrations/0001_initial.py`, `demo_shell.py`.
- №4: `tasks/admin.py`, суперпайдаланушы, Admin CRUD, іздеу және сүзгі.

`manage.py` командаларды орындайды; `settings.py` конфигурацияны сақтайды;
`urls.py` URL-ді view-ға сәйкестендіреді; `views.py` сұранысқа жауап дайындайды.

## №2 Python тізімі режимі

```powershell
$env:TASKS_USE_DB = '0'
python manage.py runserver
```

Үш демонстрациялық тапсырма Python тізімінен қайтарылады. №3–4 үшін серверді тоқтатып,
`$env:TASKS_USE_DB = '1'` орнатыңыз немесе `Remove-Item Env:TASKS_USE_DB` орындаңыз.
SQLite режимі әдепкіде қосылған.

## ORM және Admin әрекеттерін қайталау

Жаңа, тапсырмалар кестесі бос база үшін:

```powershell
python manage.py shell -c "exec(open('demo_shell.py', encoding='utf-8').read())"
```

Скрипт Shell арқылы бес тапсырма жасайды, фильтрлейді, сұрыптайды, біреуін өзгертеді,
біреуін жояды. Одан кейін Django test Client көмегімен нақты URL және Admin формаларына
HTTP сұраныстарын жібереді; Admin CSRF тексеруі қосулы. Демо суперпайдаланушыға кездейсоқ
құпиясөз жасалады; оны браузер арқылы қолдану үшін `python manage.py changepassword demo_admin`
орындаңыз. Скрипт бастапқы деректерді жоғалтпау үшін бос емес Task кестесінде тоқтайды.
`evidence/` қалтасында орындалған сұраныстар нәтижелері берілген.

## Сұраныстар

```powershell
curl.exe -i http://127.0.0.1:8000/health/
curl.exe -i http://127.0.0.1:8000/tasks/999/
Set-Content -Encoding ascii echo.json '{"message":"Hello","number":4}'
curl.exe -i -X POST http://127.0.0.1:8000/echo/ -H "Content-Type: application/json" --data-binary '@echo.json'
Set-Content -Encoding ascii invalid.json '{bad}'
curl.exe -i -X POST http://127.0.0.1:8000/echo/ -H "Content-Type: application/json" --data-binary '@invalid.json'
```

`/echo/` оқу мақсаты үшін ғана `csrf_exempt` қолданады. CSRF middleware және Admin қорғауы
қосулы. Echo JSON мәнін өзгертпей қайтарады; бос орындар мен JSON сериализациясы өзгеруі мүмкін.

## Тексеру

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test tasks -v 2
```

## Git репозиторийі

https://github.com/vhv3840-star/django-taskmanager-1-4

```powershell
git clone https://github.com/vhv3840-star/django-taskmanager-1-4.git
cd django-taskmanager-1-4
```

Репозиторий жабық. Оны клондау үшін аккаунтқа кіру және репозиторийге қолжетімділік қажет.
Дерекқор, виртуалды орта, IDE баптаулары және құпиясөздер Git-ке қосылмайды.
Бұл жоба жергілікті оқу жұмысына арналған.

## Ресми құжаттама

- https://docs.djangoproject.com/en/5.2/intro/tutorial01/
- https://docs.djangoproject.com/en/5.2/ref/request-response/
- https://docs.djangoproject.com/en/5.2/topics/db/queries/
- https://docs.djangoproject.com/en/5.2/topics/migrations/
- https://docs.djangoproject.com/en/5.2/ref/contrib/admin/
- https://docs.djangoproject.com/en/5.2/ref/csrf/

## PyCharm және есеп суреттері

PyCharm ішінде осы қалтаны жоба ретінде ашып, Python интерпретаторы ретінде
`.venv\Scripts\python.exe` таңдаңыз. `.venv` архивке қосылмайды, оны жоғарыдағы
командалармен жасаңыз. `screenshots/` ішіндегі 18 PNG — осы бағдарламадан түсірілген
нақты суреттер. Curl жауаптары `evidence/curl-valid.txt` және `curl-invalid.txt` ішінде.

`practice1.py` орта мен баптауларды тексереді. `check_task1.py` іске қосылған
8000 портындағы сервердің Health жауабын тексереді. `practice2.py` Python тізімі режиміндегі
8001 портындағы серверге сұраныстар жібереді. `practice3.py` бос Task кестесінде
миграция және бес жазбамен ORM демонстрациясын орындайды. `practice4.py` үшін
`screenshot_admin` атымен өз суперпайдаланушыңызды жасаңыз; бұл скрипт Django test Client
арқылы Admin HTTP формаларын тексереді. `practice_tests.py` 14 тестті іске қосады.

Admin браузер интерфейсінің суреті алынбады: браузер құралы жергілікті бетті ашуды
бұғаттады. Admin CRUD нәтижелері нақты HTTP формалары мен тесттер арқылы көрсетілген.
