# Restaurant Table Allocation Engine

This file explains how to run and use the project.

## 1. What this project does

This is a restaurant reservation system.

A guest enters:

- Name
- Phone number
- Party size
- Fixed dining time slot

The system automatically chooses the best available table.

The staff can use Django Admin to manage tables, time slots, and reservations.

## 2. Start the project

Open a terminal and run these commands exactly:

```bash
cd "/home/prakash/Documents/resturent teble allicotion project/project-starter/src"
source .venv/bin/activate
python manage.py migrate
python manage.py runserver
```

Keep this terminal open while using the website.

You should see a message similar to:

```text
Starting development server at http://127.0.0.1:8000/
```

If you see `port is already in use`, the server is already running. Do not start another one.

## 3. Open the website

Open this address in your browser:

```text
http://127.0.0.1:8000/
```

This is the guest reservation page.

## 4. Create the first tables and time slots

Before making a reservation, add tables and time slots through the admin page.

Open:

```text
http://127.0.0.1:8000/admin/
```

Sign in with the superuser account created during setup:

- Username: `staff`
- Password: the password you chose

In the admin page:

1. Open **Tables**.
2. Click **Add Table**.
3. Add tables such as table 1 with capacity 2, table 2 with capacity 4, and table 3 with capacity 6.
4. Add a zone such as `quiet`, `window`, or `main`.
5. Make sure **Is active** is selected.
6. Open **Time slots**.
7. Add slots such as `6-8 PM` and `8-10 PM`.
8. Set each slot's start and end time.
9. Make sure **Is active** is selected.

## 5. Make a guest reservation

Return to:

```text
http://127.0.0.1:8000/
```

Fill in the form and click **Find my table**.

If a suitable table is available, the system displays a confirmation such as:

```text
Reservation confirmed at Table 1.
```

If no table is large enough or all suitable tables are already occupied, the system displays an error instead.

## 6. How the allocation algorithm works

The algorithm first removes tables that cannot be used:

- Inactive tables are ignored.
- Tables already booked for the selected time slot are ignored.
- Tables smaller than the party are ignored.

For every remaining table, it calculates:

```text
unused seats = table capacity - party size
```

It chooses the table with the fewest unused seats.

Example:

| Table | Capacity | Party size | Unused seats |
|---|---:|---:|---:|
| Table 1 | 2 | 2 | 0 |
| Table 2 | 4 | 2 | 2 |
| Table 3 | 6 | 2 | 4 |

The system chooses **Table 1** because it fits exactly and does not waste seats.

This is called a greedy best-fit strategy. It makes the best decision for the current reservation. It cannot know future reservations, so it may not always produce the perfect allocation for the whole evening.

The main algorithm is in:

```text
ai/allocation.py
```

## 7. View the staff allocation board

The allocation board displays reservations for one time slot.

Its URL format is:

```text
http://127.0.0.1:8000/allocation/TIME_SLOT_ID/
```

For example, if the time slot ID is `1`, open:

```text
http://127.0.0.1:8000/allocation/1/
```

You can find the time slot ID in the admin page or database.

The board shows:

- Guest name
- Party size
- Assigned table
- Reservation status

## 8. Important project files

| File | Purpose |
|---|---|
| `src/core/models.py` | Database models for tables, time slots, and reservations |
| `src/core/forms.py` | Guest reservation form |
| `src/core/views.py` | Booking and allocation-board workflow |
| `src/core/urls.py` | Website URLs |
| `src/core/admin.py` | Admin page configuration |
| `src/templates/core/booking.html` | Guest booking page |
| `src/templates/core/allocation_board.html` | Staff allocation board |
| `src/core/static/core/styles.css` | Website styling |
| `ai/allocation.py` | Greedy table-selection algorithm |
| `ai/search.py` | Search algorithm learning module |
| `src/db.sqlite3` | Local database created by Django |

## 9. Run tests

From the `src` directory, run:

```bash
.venv/bin/python manage.py test core
```

You should see:

```text
Ran 3 tests
OK
```

You can also check the whole Django project:

```bash
.venv/bin/python manage.py check
```

Expected result:

```text
System check identified no issues (0 silenced).
```

## 10. Stop the server

Go to the terminal running Django and press:

```text
Ctrl + C
```

## 11. Start it again later

Every time you want to use the project again:

```bash
cd "/home/prakash/Documents/resturent teble allicotion project/project-starter/src"
source .venv/bin/activate
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## 12. Common problems

### `cd: src: No such file or directory`

You are already inside the `src` folder. Run:

```bash
source .venv/bin/activate
python manage.py runserver
```

### `port is already in use`

A server is already running. Open the website instead of starting another server:

```text
http://127.0.0.1:8000/
```

### The page looks like plain text

Refresh with:

```text
Ctrl + Shift + R
```

Make sure the server is running and open the main URL again.

### `No suitable table is available`

Add a table with enough capacity, or choose a different time slot.

### Forgot the admin password

From the `src` directory, run:

```bash
.venv/bin/python manage.py changepassword staff
```

Then enter a new password when Django asks.
