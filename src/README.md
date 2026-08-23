# src/ — your Django project goes here

This folder is empty on purpose: you create the Django project yourself in the lab sessions (that's part of the learning, not busywork).

## One-time setup, per machine

**1. Install PostgreSQL** (once per computer) and make sure it's running:

- macOS: `brew install postgresql@16 && brew services start postgresql@16`
- Windows: installer from https://www.postgresql.org/download/windows/ (remember the password you set for the `postgres` user)
- Linux: `sudo apt install postgresql` then `sudo systemctl start postgresql`

**2. Create your project's database** (once per machine):

```sh
createdb projectdb        # if this fails on Windows/Linux, try: psql -U postgres -c "CREATE DATABASE projectdb;"
```

**3. Create the Django project:**

```sh
cd src
python -m venv .venv           # once
source .venv/bin/activate      # every session (Windows: .venv\Scripts\activate)
pip install django "psycopg[binary]"
django-admin startproject config .
python manage.py startapp core
```

**4. Point Django at PostgreSQL** — in `config/settings.py`, replace the `DATABASES` block:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "projectdb",
        "USER": "postgres",        # or your own username on macOS/Linux
        "PASSWORD": "",            # whatever you set during install (often empty on macOS)
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

Then `python manage.py migrate` — if it runs without errors, Django and PostgreSQL are talking. That's your ✓ for the setup.

## Daily commands

```sh
source .venv/bin/activate         # start of every session
python manage.py makemigrations   # after changing models.py
python manage.py migrate          # apply changes to the PostgreSQL database
python manage.py createsuperuser  # once, for /admin/
python manage.py runserver        # -> http://127.0.0.1:8000
```

Want to see your actual tables? `psql projectdb` then `\dt` — the [PostgreSQL 101](https://learn.kevalabs.com/databases/postgresql-101/) guide teaches you the rest of that world.

Your views import the AI module like any other Python code:

```python
from ai.search import search, take_bfs   # or: from ai.rules import recommend
```

📖 Read: [How Python packages work](https://learn.kevalabs.com/python/fundamentals/how-python-packages-work/) (venv, pip) · [How Django works](https://learn.kevalabs.com/python/django/how-django-works/)
