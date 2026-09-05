# Restaurant Table Allocation

A Django application for managing restaurant reservations and table allocation.

## Start the application

From the project root:

```sh
cd src
source .venv/bin/activate
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in your browser.

On Windows, activate the virtual environment with:

```powershell
.venv\Scripts\activate
```

## Useful commands

```sh
cd src
source .venv/bin/activate
python manage.py createsuperuser  # optional, for /admin/
python manage.py test
```

The project uses SQLite, stored in `src/db.sqlite3`. Stop the development server with `Ctrl+C`.
