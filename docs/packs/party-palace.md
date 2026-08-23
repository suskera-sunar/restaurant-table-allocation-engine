# Project pack — Grand Venue Scheduling & Vendor Cost Optimizer

> **AI component: A\* over vendor assignments with an admissible cheapest-remaining heuristic.**
> Copy this file to `docs/project-pack.md`, delete the other packs, commit. This pack is your single source of truth for scope — check every "can it also…?" against the out-of-scope list. **Yours is the most ambitious AI of the four cohorts — the scope below is tight on purpose. Hold the line.**

## The idea

Customers request an event: a date, a guest count, a budget, and which services they need (catering, decoration, music). The system books a hall with enough capacity on a free date, then the intelligent part: **A\*** finds the *cheapest combination of vendors* covering the requested services within budget — provably cheapest, not just plausible.

## Users

| Who | Does |
|---|---|
| Customer | submits an event request: name, phone, date, guests, budget, services needed (no login) |
| Staff | one login; sees the booking calendar (list, not a drawn calendar) and each event's optimized vendor plan |
| Admin | manages halls, the three service types, and vendors with prices in Django admin |

## Minimal scope

| Must have | Nice to have | Out of scope |
|---|---|---|
| Event request form (**date, not time**; services as 3 checkboxes) | Vendor quality score as tie-breaker | More than 3 service types (hold the line here) |
| Hall booking: one event per hall per date | "Over budget by ₨X" message with the cheapest anyway | Vendor availability calendars |
| **A\* cheapest vendor combination within budget** | Compare top-2 combinations | Multi-day events, time-of-day slots |
| Staff view: bookings + vendor plan per event | | Invoices, partial payments, discounts |
| Admin-managed halls, services, vendors+prices | | Guest lists, seating |

## Data model (→ your Django models)

- **Hall** — name, capacity
- **ServiceType** — name (exactly three rows: catering, decoration, music)
- **Vendor** — name, service (FK), price
- **EventRequest** — customer_name, phone, date, guests, budget, hall (FK), status
- **EventService** — event (FK), service (FK) ← which services were requested
- **VendorAssignment** — event (FK), vendor (FK) ← what A\* chose

## The AI formulation (memorize this — it's the best exam answer in the course)

- **State:** the set of services already assigned a vendor (start: none assigned; goal: all requested services assigned).
- **Actions:** assign one of the available vendors to the next unassigned service.
- **g(state):** money committed so far — the sum of chosen vendors' prices.
- **h(state):** sum of the *cheapest* vendor's price for each still-unassigned service.
- **Admissible because** no service can ever be filled below its cheapest option — h never overestimates, therefore A\* returns the provably cheapest combination.
- Start from `ai/search.py` — implement A\*'s `take()` (minimum g + h), then model states as frozensets of (service, vendor) pairs.

**Honesty check (the viva will probe this):** with 3 services × V vendors, brute force is V³ combinations — small! So why A\*? Answer honestly: at this size brute force works, but A\* scales when services or constraints grow, and the *formulation* (state/g/h, admissibility) is the point of the exercise. Also rehearse: "what if h overestimated?" (optimality lost) and "what if h = 0?" (Dijkstra — correct but explores more).

## Reading order

1. The whole [python-web roadmap](https://learn.kevalabs.com/roadmaps/python-web/) with the lab sessions
2. [How AI search works](https://learn.kevalabs.com/ai/how-search-algorithms-work/) — greedy and A\* sections closely; your exact formulation ("sum of each remaining service's cheapest vendor") appears there as the worked example of building admissible heuristics

## Pitfalls (teams before you fell in these)

- **Three services. Three.** Every additional service type multiplies the state space and your testing burden; the syllabus marks your formulation, not your feature count.
- Dates, not times. One event per hall per date makes the availability check a single database lookup.
- Seed vendors so the optimum is *not* obvious (make the cheapest caterer pair badly with the budget so the second-cheapest wins overall) — a demo where A\* finds a non-obvious answer is dramatically more convincing.
- Budget exceeded? Still show the cheapest combination with a clear "over budget by ₨X" — a dead-end demo ("no result") reads as a bug even when it's correct.
