# Software Requirements Specification (SRS)

> **Milestone 2.** The SRS answers one question precisely: *what will the software do?* — not how. If a sentence mentions Django, a table schema, or an algorithm's internals, it belongs in the design docs, not here. Replace every *[bracketed instruction]*, delete rows you don't need, add rows you do.

## 1. Introduction

### 1.1 Purpose
*[Two sentences: what system this SRS describes, and who the document is for (your team, your supervisor, the external examiner).]*

### 1.2 Intended users
*[Who touches the system? Almost every team has exactly three: the **customer/member** (public, no login), the **staff** (one login), and the **admin** (Django admin). Describe what each one wants in one line.]*

### 1.3 Definitions
*[Terms someone outside your domain wouldn't know. "Prep step: one kitchen action required before an item can be served." 3–6 entries.]*

## 2. Overall description

*[One paragraph: the system from 10,000 feet — what flows in, what flows out, where the intelligent component sits in that flow. Reference the system flowchart in `flowcharts.md` rather than repeating it.]*

📖 Read: [How HTTP works](https://learn.kevalabs.com/web-fundamentals/how-http-works/) — requests and responses are the vocabulary this section is written in.

## 3. Functional requirements

*[The heart of the SRS. Each row: an ID you can cite later ("as required by FR-3…"), one capability, one priority. Copy your must-have list from `project-pack.md` and turn each feature into 1–3 rows. Rules of thumb: if it has an "and" in it, split it; if you can't demo it, reword it until you can.]*

| ID | Requirement | Priority |
|---|---|---|
| FR-1 | The system shall let the customer view *[…]* | Must |
| FR-2 | The system shall let the customer submit *[…]* with name and phone number | Must |
| FR-3 | The system shall let staff view *[…]* and update its status | Must |
| FR-4 | The system shall let the admin manage *[…]* via the admin panel | Must |
| FR-5 | The system shall compute *[your AI output]* from *[your AI input]* | Must |
| FR-6 | *[nice-to-have, only if weeks 10–12 go well]* | Could |

## 4. The intelligent component's contract

*[Specify your AI module like a function — inputs, outputs, and rules it must obey — WITHOUT describing the algorithm (that's the report's job). Example for a scheduler: "Input: the set of pending orders and the prep-dependency list. Output: an ordered list of batches such that no item appears before its dependencies. Constraint: every pending item appears exactly once."]*

- **Input:** *[…]*
- **Output:** *[…]*
- **Constraints the output must satisfy:** *[…]*

## 5. Non-functional requirements

*[Keep this honest and small — beginner projects claiming "99.9% uptime" get laughed at in vivas. These four are usually enough:]*

| ID | Requirement |
|---|---|
| NFR-1 | Any page responds within *[2]* seconds on the lab machines |
| NFR-2 | Staff pages require login; customer pages do not |
| NFR-3 | Submitted data survives a server restart (stored in the database, not memory) |
| NFR-4 | The AI module runs standalone via `python ai/search.py` *(or `rules.py`)* for demonstration |

📖 Read: [How auth works](https://learn.kevalabs.com/security/authentication-vs-authorization/) — NFR-2 is an authorization statement; know the difference before the viva.

## 6. Data requirements

*[List your entities and one line each on what they represent — the full ER diagram lives in `flowcharts.md`, the field-by-field detail in your project-pack. "Order: one customer's request, with a status that moves Placed → Preparing → Ready."]*

📖 Read: [PostgreSQL 101](https://learn.kevalabs.com/databases/postgresql-101/) — tables, rows, and keys; the concepts are identical in SQLite.

## 7. Interface requirements

*[List every page/screen with one line: URL path, who uses it, what's on it. If this list exceeds ~7 rows, your scope has crept — cut it back.]*

| Page | Who | Shows / does |
|---|---|---|
| `/` | customer | *[…]* |
| `/…` | customer | *[…]* |
| `/staff/…` | staff | *[…]* |
| `/admin/` | admin | Django admin (built in) |
