# Project pack — Smart Restaurant Table Allocation Engine

> **AI component: greedy best-first choice with a capacity-fit heuristic.**
> Copy this file to `docs/project-pack.md`, delete the other packs, commit. This pack is your single source of truth for scope — check every "can it also…?" against the out-of-scope list.

## The idea

Guests request a reservation (party size + time slot); the system assigns the *best* free table using a heuristic — not just *any* table. Booking a party of 2 onto the last 6-seat table wastes seats the 6-person party at 8pm needed; your greedy module scores every free table and picks the tightest fit. Staff see the evening's allocation at a glance.

## Users

| Who | Does |
|---|---|
| Guest | requests a reservation: name, phone, party size, time slot (no login) |
| Staff | one login; sees per-slot allocation board, marks no-shows/frees tables |
| Admin | manages tables (capacity, zone tag) and the slot list in Django admin |

## Minimal scope

| Must have | Nice to have | Out of scope |
|---|---|---|
| Reservation form with **fixed time slots** (e.g. 6–8pm, 8–10pm) | Zone preference (window/quiet) as heuristic tie-breaker | Free-form times (this is where complexity hides — refuse it) |
| **Greedy allocation on submit** | Walk-in entry by staff | Table merging for large parties |
| Staff allocation board per slot | Cancellation | Floor-plan drawing, SMS/email, deposits |
| Admin-managed tables + slots | Reject-with-reason when full | Waitlists |

## Data model (→ your Django models)

- **Table** — name/number, capacity, zone
- **TimeSlot** — label, start, end
- **Reservation** — guest_name, phone, party_size, slot (FK), table (FK, set by the algorithm), status, created_at

## The AI formulation (memorize this)

- **Candidates:** tables free in the requested slot with `capacity >= party_size`.
- **Heuristic:** `h(table) = capacity − party_size` — smaller is better (tightest sufficient fit); optional tie-breaker on zone preference.
- **Choice:** take the candidate with minimum h. That's greedy best-first: rank by the heuristic, commit, never look back.
- Start from `ai/search.py` — implement the greedy `take()` there first to *learn* the discipline, then write your allocator as a scoring function over candidate tables.

**Honesty check (the viva will probe this):** greedy can be beaten — giving a party of 2 the last 4-seat table just before a party of 4 calls. Know your failure mode AND your defense: future requests are unknown, so per-arrival greedy with tight-fit scoring is the standard practical answer; optimal offline assignment would need all requests in advance.

## Reading order

1. The whole [python-web roadmap](https://learn.kevalabs.com/roadmaps/python-web/) with the lab sessions
2. [How AI search works](https://learn.kevalabs.com/ai/how-search-algorithms-work/) — especially the greedy best-first section (your algorithm) and the A* section (so you can answer "why didn't you need A*?" — you have no path cost accumulating; each allocation is a single scored choice)

## Pitfalls (teams before you fell in these)

- **Fixed slots are non-negotiable.** Continuous times turn "is the table free?" into interval-overlap mathematics — a whole project by itself.
- Do the capacity check *before* scoring; a 2-seat table must never appear as a candidate for a party of 4, however good its score.
- Demo with a full evening seeded: ~8 tables, ~12 reservations, one request that gets rejected because nothing fits. The rejection is proof your candidate filter works — show it proudly.
