# Project pack — Gym Membership Ledger & Workout Scheduler

> **AI component: backward chaining over a rule base (expert system).**
> Copy this file to `docs/project-pack.md`, delete the other packs, commit. This pack is your single source of truth for scope — check every "can it also…?" against the out-of-scope list.

## The idea

Staff keep the gym's books: members, plans, expiry dates, and a simple payment ledger. The intelligent part is the **workout recommender**: an expert system that interviews a member (goal? experience? days per week?) and recommends a plan by reasoning *backward* from the question — asking only the questions the answer actually depends on, exactly like a good trainer would.

## Users

| Who | Does |
|---|---|
| Member | answers the recommender's interview on a public page (no login) |
| Staff | one login; manages member records, enters ledger payments, sees expiring-soon list |
| Admin | manages membership plans and the **rules** of the recommender in Django admin |

## Minimal scope

| Must have | Nice to have | Out of scope |
|---|---|---|
| Member CRUD with plan + expiry | Attendance check-in (one button) | Payment gateway (ledger = typed rows) |
| Payment ledger (member, amount, date) | Receipt print view | Progress tracking, measurements |
| "Expiring this week" staff list | Rules editable in admin (vs in code) | Diet plans, exercise videos |
| **Backward-chaining recommender interview** | "Why?" link showing the proof chain | Per-exercise customization |
| Weekly plan template shown for the result | | Member logins |

## Data model (→ your Django models)

- **Plan** — name, price, duration_months
- **Member** — name, phone, plan (FK), joined, expires
- **LedgerEntry** — member (FK), amount, date, note
- **WorkoutPlan** — name, weekly_template (text shown when recommended)
- *(if rules go in the DB — the nice-to-have)* **Rule** — conclusion, conditions (comma-separated); otherwise rules live in `ai/rules.py` as a Python list

## The AI formulation (memorize this)

- **Knowledge base:** 10–15 IF–THEN rules from a real trainer's logic, layered so rules chain (e.g. `goal: weight loss AND 3+ days` → `cardio focus`; `cardio focus AND beginner` → `plan: full-body circuit`).
- **Engine:** backward chaining — start from "which plan?", find rules concluding a plan, prove each condition recursively; a condition no rule concludes is a *leaf* → ask the member, right then.
- **Interview:** the questions ARE the algorithm running. Failed branches short-circuit, so members are never asked irrelevant questions.
- Start from `ai/rules.py` — the engine is written; **your work is the rules.** Interview a real trainer (or be honest that you invented them, and say so in the report).

**Honesty check (the viva will probe this):** why backward and not forward chaining? One question wanted, not all consequences — backward asks only what the goal needs. And know that the engine is DFS over an AND/OR proof tree: read the search guide's DFS section or you'll be caught by the cross-question.

## Reading order

1. The whole [python-web roadmap](https://learn.kevalabs.com/roadmaps/python-web/) with the lab sessions
2. [How AI search works](https://learn.kevalabs.com/ai/how-search-algorithms-work/) — the DFS section minimum
3. [How expert systems work](https://learn.kevalabs.com/ai/how-expert-systems-work/) — your whole algorithm, including the 15-line engine you'll extend

## Pitfalls (teams before you fell in these)

- **Fewer than ~10 rules looks like a quiz, not an expert system.** The credibility comes from rules that *chain* — at least two intermediate concepts (like `cardio focus`) that no user is ever asked about directly.
- The interview must be dynamic: hardcoding all questions on one form is forward chaining with extra steps, and the examiners know it. Ask one question per page, chosen by the engine.
- The ledger is deliberately boring — typed rows, no gateway. Every hour spent making payments fancy is an hour stolen from the recommender, which is where your marks are.
