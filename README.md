# project-starter

Starter template for the Python software project course. It gives your team every document you must submit — proposal, SRS, flowcharts, report, presentation outline, viva prep — as **fill-in-the-blank templates**, plus stubs for the AI module your project includes. Each section links to the [learn.kevalabs.com](https://learn.kevalabs.com) guide that teaches the concept you need to fill it in.

You don't start from a blank page. You start from here.

## How to use this repo

1. One team member clicks **Use this template → Create a new repository** (name it after your project, e.g. `cafe-order-engine`). Make it private if you like, and add your teammates as collaborators.
2. Everyone clones it. New to Git? Read [How Git works](https://learn.kevalabs.com/computer-fundamentals/how-git-works/) first.
3. **First assignment (do it now):** find your project's pack in [`docs/packs/`](docs/packs/), copy it to `docs/project-pack.md`, delete the other three packs, commit, and push. Congratulations — your repo is now *your project's* repo, and you've made your first team commit.
4. Work through the milestones below. Every document in `docs/` tells you what to write and what to read.

## What's where

| Path | What it is | When you need it |
|---|---|---|
| `docs/project-pack.md` | Your project's scope, data model, and AI formulation | Day 1, then constantly |
| `docs/proposal.md` | Proposal template | Milestone 1 |
| `docs/srs.md` | Software Requirements Specification template | Milestone 2 |
| `docs/flowcharts.md` | Flowchart + ER diagram starters (Mermaid — renders on GitHub) | Milestone 2 |
| `docs/report.md` | Final project report template | Milestone 4 |
| `docs/presentation.md` | Mid-term and final presentation outlines | Milestones 3 & 4 |
| `docs/viva-prep.md` | Questions the examiners will ask, with where to find answers | Before the viva |
| `ai/search.py` | Frontier-loop search skeleton (BFS done; DFS, greedy, A* are yours) | Cafe, Restaurant, Party Palace teams |
| `ai/rules.py` | Backward-chaining engine (engine done; the rules are yours) | Gym team |
| `src/` | Your Django project lives here — you create it in the lab sessions | From the CRUD milestone on |

## Milestones (mapped to your marks)

**Internal — 60 marks**

- [ ] **M1 · Proposal (10 marks)** — `docs/proposal.md` complete, topic approved by supervisor.
- [ ] **M2 · Requirements & design** — `docs/srs.md` and `docs/flowcharts.md` complete. (Not separately marked, but the mid-term presentation is built from these.)
- [ ] **M3 · Mid-term presentation (20 marks)** — working CRUD demo + AI module plan. Outline in `docs/presentation.md`.
- [ ] **M4 · Pre-final submission & final presentation (30 marks)** — working app with AI module integrated, report drafted, demo rehearsed.

**External — 40 marks**

- [ ] **M5 · Project documentation (20 marks)** — `docs/report.md` finished and printed.
- [ ] **M6 · Final presentation (10 marks)** — same demo, tighter.
- [ ] **M7 · Viva (10 marks)** — every member can answer everything in `docs/viva-prep.md`.

## Ground rules (agreed scope for all teams)

These keep the project finishable in 45 hours. Breaking them needs supervisor approval, and the answer is probably no:

- **Django + SQLite**, server-rendered templates only. No JavaScript frameworks, no REST APIs, no real-time features.
- **Django admin is your back-office.** Menu items, tables, plans, vendors — managed there, not in hand-built screens.
- **No payments, no email/SMS, no user registration.** At most one staff login. Customer-facing forms take a name and phone number.
- **The AI part is a pure-Python module** (`ai/`) with plain functions your views call. It must run and be demonstrable on its own, without Django.

## Reading path

The guides are ordered for you in the [From zero to your first Python web project](https://learn.kevalabs.com/roadmaps/python-web/) roadmap — follow it alongside the lab sessions. Your AI reading depends on your team:

- Cafe, Restaurant, Party Palace → [How AI search works](https://learn.kevalabs.com/ai/how-search-algorithms-work/)
- Gym → [How expert systems work](https://learn.kevalabs.com/ai/how-expert-systems-work/) (read the search guide first — backward chaining is DFS)
