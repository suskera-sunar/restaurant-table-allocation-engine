# Project pack — Dynamic Cafe Menu & Order Booking Engine

> **AI component: breadth-first search (BFS) over the prep-dependency graph.**
> Copy this file to `docs/project-pack.md`, delete the other packs, commit. This pack is your single source of truth for scope — when anyone (including you) suggests a new feature, check it against the out-of-scope list first.

## The idea

Customers browse the cafe's menu and place an order from their table. Staff see incoming orders and move them through Placed → Preparing → Ready. The intelligent part: the kitchen doesn't prepare items in arrival order — some items depend on prep steps (dough before pizza, patty before burger), and your BFS module computes which items can be prepared **in parallel, in batches**, from the dependency graph.

## Users

| Who | Does |
|---|---|
| Customer | views menu, places an order (name + table number, no login) |
| Staff | one login; sees order queue, advances status, sees the prep-batch plan |
| Admin | manages menu items, categories, and prep dependencies in Django admin |

## Minimal scope

| Must have | Nice to have | Out of scope |
|---|---|---|
| Menu page grouped by category | Item photos | Payments of any kind |
| Order form (items + name + table) | Daily specials flag | Customer accounts / order history |
| Staff queue with status buttons | Order cancellation | Inventory tracking |
| Admin-managed menu + dependencies | Estimated prep times | Real-time updates (refresh is fine) |
| **BFS prep-batch view for staff** | | Delivery, tables map, printing |

## Data model (→ your Django models)

- **Category** — name
- **MenuItem** — name, price, available, category (FK)
- **PrepStep** — name (e.g. "grill patty", "assemble burger")
- **Dependency** — step (FK), must_come_after (FK to PrepStep) ← *this is the graph's edge list*
- **MenuItem ↔ PrepStep** — which steps an item needs (many-to-many)
- **Order** — customer_name, table_number, status, created_at
- **OrderLine** — order (FK), item (FK), quantity

## The AI formulation (memorize this)

- **Graph:** nodes = prep steps needed by the current pending orders; edges = "must come after" dependencies.
- **BFS levels = the schedule:** level 0 is every step with no unfinished prerequisite (start all of these in parallel now); level 1 is everything unlocked when level 0 finishes; and so on.
- **Output:** an ordered list of batches, each batch a set of steps that can run simultaneously.
- Start from `ai/search.py` — the frontier loop is there; your work is building the graph from the database and reading the levels off BFS.

**Honesty check (the viva will probe this):** why BFS and not a simple loop? Because dependencies chain arbitrarily deep — only level-order traversal guarantees nothing starts before its prerequisites, whatever graph the admin configures. Know this answer cold.

## Reading order

1. The whole [python-web roadmap](https://learn.kevalabs.com/roadmaps/python-web/) with the lab sessions
2. [How AI search works](https://learn.kevalabs.com/ai/how-search-algorithms-work/) — especially the BFS section's "dependency levels" paragraph and the frontier-loop simulator

## Pitfalls (teams before you fell in these)

- **BFS must earn its place.** If your dependency graph has 2 nodes, the examiners will ask why you needed an algorithm. Seed the demo menu with a realistic graph — 8–12 prep steps, chains 3 deep.
- Don't build a table map, a kitchen display with auto-refresh, or per-item timers. The batch list is the feature.
- Circular dependencies (A after B after A) will hang naive code — detect them (BFS finishing without visiting every node = a cycle exists) and show a friendly admin error. Cheap to do, very impressive in the viva.
