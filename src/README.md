# src/ — your Django project goes here

This folder is empty on purpose: you create the Django project yourself in the lab sessions (that's part of the learning, not busywork). When the time comes:

```sh
cd src
python -m venv .venv           # once
source .venv/bin/activate      # every session (Windows: .venv\Scripts\activate)
pip install django
django-admin startproject config .
python manage.py startapp core
python manage.py runserver     # -> http://127.0.0.1:8000
```

Daily commands you'll use constantly:

```sh
python manage.py makemigrations   # after changing models.py
python manage.py migrate          # apply changes to db.sqlite3
python manage.py createsuperuser  # once, for /admin/
python manage.py runserver
```

Your views import the AI module like any other Python code:

```python
from ai.search import search, take_bfs   # or: from ai.rules import recommend
```

📖 Read: [How Python packages work](https://learn.kevalabs.com/python/fundamentals/how-python-packages-work/) (venv, pip) · [How Django works](https://learn.kevalabs.com/python/django/how-django-works/)
