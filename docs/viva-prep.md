# Viva preparation

> **Milestone 7 — 10 marks.** The viva is a conversation, not a quiz: examiners pull one thread ("why Django?") and follow it down ("so what's a view?" … "and what does the ORM do with that?"). The defense is understanding *why*, not memorizing answers. Every answer below is a starting point — practice saying them in your own words, out loud, to each other. The 📖 link is where the full explanation lives.
>
> **Ironclad rule:** every member must be able to answer every general question, and *anyone* may be asked about the AI module — not just whoever wrote it.

## About your project (asked first, sets the tone)

**Q. Explain your project in one minute.**
Problem → users → what the software does → where the intelligence is. Practice this until it's smooth; a fumbled opener colors the whole viva. (Your proposal §3 + §7, compressed.)

**Q. Why did you choose this project?**
Have a real answer — a domain you knew, a problem you'd seen. "The teacher assigned it" scores zero.

**Q. What was the hardest part, and how did you solve it?**
Prepare one true story with a technical core (a bug, the AI formulation, a data-model rework). Honest struggle + resolution is exactly what they want to hear.

**Q. Who wrote which part?**
Answer must match the report's contribution table *and* your Git history.

## Python and OOP

**Q. Why Python? / Why Django?**
Python: one readable language for both the web app and the AI module; batteries included. Django: routing, ORM, forms, admin, and auth are built in — a 3-person beginner team ships in 45 hours instead of reinventing plumbing. 📖 [How Django works](https://learn.kevalabs.com/python/django/how-django-works/)

**Q. Where is OOP in your project?**
Point at your models: each entity is a class, each row an object; methods hold the entity's behavior (e.g. `order.total()`). Know the words *class, object, attribute, method, inheritance* — and show where inheritance actually appears: every model inherits from `models.Model`. 📖 [Object-oriented Python](https://learn.kevalabs.com/python/fundamentals/object-oriented-python/)

**Q. What is a virtual environment and why did you use one?**
An isolated per-project package set, so your project's Django version can't clash with another project's. 📖 [How Python packages work](https://learn.kevalabs.com/python/fundamentals/how-python-packages-work/)

## Web and Django

**Q. What happens when a user submits the order form? Walk me through it.**
Browser sends an HTTP POST → Django's URL router matches the path to a view → the form validates the data (re-shown with errors if invalid) → the view saves via the model → the ORM writes an SQL INSERT to PostgreSQL → the view returns rendered HTML. Practice this chain — it's the single most-asked viva question for web projects. 📖 [How HTTP works](https://learn.kevalabs.com/web-fundamentals/how-http-works/) · [How Django works](https://learn.kevalabs.com/python/django/how-django-works/)

**Q. What is CSRF and how does your project handle it?**
A forged cross-site submission riding on a logged-in user's cookies; Django's `{% csrf_token %}` puts a secret in each form and rejects POSTs without it. 📖 [How HTML forms work](https://learn.kevalabs.com/web-fundamentals/how-html-forms-work/)

**Q. Authentication vs authorization — which does your staff page use?**
Authentication = who you are (the login). Authorization = what you may do (`@login_required` on staff views). The staff page uses both. 📖 [How auth works](https://learn.kevalabs.com/security/authentication-vs-authorization/)

**Q. Why server-side rendering and not a JavaScript frontend?**
One language, one codebase, simpler mental model, and our pages are forms-and-lists — SSR is the right tool, not just the easy one. 📖 [Server-side vs client-side rendering](https://learn.kevalabs.com/web-fundamentals/server-side-vs-client-side-rendering/)

## Database

**Q. Show me your ER diagram. Why is this relationship one-to-many?**
Rehearse on your actual diagram: "one Category contains many Items because…". Know where the foreign key lives (on the *many* side).

**Q. What is a primary key? A foreign key?**
Primary: the column that uniquely identifies a row (Django adds `id` automatically). Foreign: a column holding another table's primary key — that's what a `ForeignKey` field becomes. 📖 [PostgreSQL 101](https://learn.kevalabs.com/databases/postgresql-101/)

**Q. What does the ORM actually do?**
Translates between objects and rows: `Order.objects.filter(status="placed")` becomes a SQL `SELECT … WHERE`. Know one example in both notations. 📖 [How ORMs work](https://learn.kevalabs.com/python/fundamentals/how-orms-work/)

**Q. Why PostgreSQL and not something simpler like SQLite?**
SQLite is a single file with one writer at a time — fine for solo development. PostgreSQL is a real client-server database: it handles several staff users writing concurrently, and it's what production systems actually run, so deploying our project needs no database change. Know the shape: PostgreSQL runs as a separate server process; Django connects to it through settings and the psycopg driver. 📖 [PostgreSQL 101](https://learn.kevalabs.com/databases/postgresql-101/) · [How deployment works](https://learn.kevalabs.com/web-fundamentals/how-deployment-works/)

## Git and teamwork

**Q. How did three people work on one codebase without overwriting each other?**
Git: everyone commits locally, pushes to the shared repo, pulls before starting. Know what a commit *is* (a snapshot, not a diff) and what a merge conflict is — bonus points for describing one you actually resolved. 📖 [How Git works](https://learn.kevalabs.com/computer-fundamentals/how-git-works/)

## The intelligent component — all teams

> 📖 Search teams: [How AI search works](https://learn.kevalabs.com/ai/how-search-algorithms-work/). Gym team: [How expert systems work](https://learn.kevalabs.com/ai/how-expert-systems-work/) — but read both; the cross-questions don't respect team boundaries.

**Q. Why is this an "intelligent system" and not just an if/else?**
Because the possibilities explode combinatorially (or the rules chain unpredictably) — no fixed if/else covers every case. The module explores/reasons *systematically* over a problem it has never seen the specific instance of. Give YOUR numbers: how many combinations does brute force face in your data?

**Q. What would brute force cost, and what does your algorithm save?**
Have the concrete comparison ready — it's the single best justification you can give.

**Q. Trace your algorithm by hand on a small example.**
The examiners may hand you paper. Practice the trace from your report §2 until any member can reproduce it.

## The intelligent component — per team

**Cafe (BFS): Why breadth-first and not depth-first?**
BFS visits states in dependency levels — level *n* is everything unlockable after level *n−1* — which is exactly a prep schedule: each ring is a batch that can run in parallel. DFS's dive order has no such meaning. Also know: queue vs stack, and why the visited set matters.

**Restaurant (greedy): What's your heuristic, and when does greedy give a bad answer?**
Score = capacity − party size (smallest sufficient table). Greedy is fooled when a locally-best choice blocks a better global assignment — e.g. giving a party of 2 the last 4-seat table just before a party of 4 arrives. Say why that's acceptable here (walk-ins are unknown; re-run per arrival) — knowing your algorithm's failure mode is worth more marks than pretending it has none.

**Gym (backward chaining): Why backward and not forward chaining?**
We have one question ("which plan?"), not a data dump wanting all consequences. Backward chaining starts from the goal and asks only what the goal needs — fewer questions, every one explainable by reading up the proof tree. Know: it's DFS over an AND/OR tree, and one failed condition prunes the whole branch.

**Party Palace (A\*): What are g, h, and f in YOUR project — and is your h admissible?**
g = money committed to vendors so far; h = sum of each remaining service's *cheapest* vendor; f = g + h. Admissible because no service can ever be booked below its cheapest option — h never overestimates, so A\* is guaranteed to find the cheapest combination. If h overestimated, it could skip the best answer. Expect the follow-up: "what happens if h = 0?" (It becomes Dijkstra — still correct, explores more.)
