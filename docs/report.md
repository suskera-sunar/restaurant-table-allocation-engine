# Project Report

> **Milestone 5 — 20 external marks**, the largest single item in your grade. The good news: if you kept the other docs current, most of this report is assembly, not writing. Sections 3–5 come from your proposal and SRS; only 6–8 are genuinely new. Replace every *[bracketed instruction]*; target 15–25 pages printed.

## Cover page

*[Project title · course name and code · team members with roll numbers · supervisor · college · date. Follow your college's required format if one exists.]*

## Acknowledgements & declaration

*[Standard college format. In the declaration, credit honestly: this repo's templates and skeleton, the learn.kevalabs.com guides, and any code you adapted. Examiners punish hidden borrowing, never acknowledged borrowing.]*

## 1. Technical description of the project

*[2–3 pages. What the system is and does, for a technical reader seeing it cold: the problem (from the proposal), the users, the main flows, and where the intelligent component sits. Include the system flowchart from `flowcharts.md` here.]*

## 2. System aspect of the project

*[The "how it's built" chapter, 3–4 pages:]*

- **Architecture** — *[browser → Django (URLs → views → models → templates) → PostgreSQL; a diagram plus a paragraph per layer. Explain server-side rendering and why it fits this project.]*
  📖 [How Django works](https://learn.kevalabs.com/python/django/how-django-works/) · [Server-side vs client-side rendering](https://learn.kevalabs.com/web-fundamentals/server-side-vs-client-side-rendering/)
- **Data model** — *[the ER diagram, then one paragraph per entity: what it stores and why the relationships are shaped that way.]*
- **The intelligent component** — *[your algorithm from first principles: the problem formulation (states/actions/goal, or rules), WHY this algorithm fits (what would brute force cost? what does yours guarantee?), and a worked example traced by hand on your real data. This subsection carries the "intelligent system" claim — make it the best-written page in the report.]*
  📖 [How AI search works](https://learn.kevalabs.com/ai/how-search-algorithms-work/) *or* [How expert systems work](https://learn.kevalabs.com/ai/how-expert-systems-work/)
- **Security** — *[half a page: which pages need login and why, what CSRF protection is and that Django's forms give it to you.]*
  📖 [How auth works](https://learn.kevalabs.com/security/authentication-vs-authorization/) · [How HTML forms work](https://learn.kevalabs.com/web-fundamentals/how-html-forms-work/)

## 3. Project tasks and time schedule

*[The schedule table from the proposal — as it actually happened. Add a "planned vs actual" column and one honest paragraph about the biggest deviation and why. Examiners trust reports that admit slippage far more than ones claiming everything went to plan.]*

## 4. Project team members

*[One row per member: name, roll number, and their actual contributions — which features, which documents. Your Git history is the evidence; keep this consistent with it, because the viva can check.]*

## 5. Project supervisor

*[Name, designation, department.]*

## 6. Implementation of the project

*[3–5 pages. Walk the working system screen by screen with screenshots. For each: what the user does, what happens underneath (one sentence), and which requirement it satisfies ("this fulfils FR-3"). Then the AI module in action: the standalone run (`python ai/search.py` output) and the integrated result in the app. Include your 3–5 most important code snippets — the AI module's core loop, one model, one view — never full listings (those go in the appendix).]*

## 7. Testing

*[1–2 pages. A table of manual test cases: what you did, what you expected, what happened — including at least two FAILURE cases you found and fixed (say what the bug was). For the AI module: the self-test in `ai/` plus one hand-checked example proving the output correct.]*

## 8. Limitations and future enhancements

*[Half a page each. Limitations: the out-of-scope list from the proposal, stated plainly. Future work: 3–4 items with one sentence on how each would be built — this shows the examiners you understand the road not taken (e.g. "deployment to a real server", "automated database backups").]*
📖 [How deployment works](https://learn.kevalabs.com/web-fundamentals/how-deployment-works/)

## References

*[APA 7th edition, alphabetized. Cite: the learn.kevalabs guides you used, the Django documentation, and your algorithm's source. Two entries to start you off — keep, and add your own:]*

- Django Software Foundation. (n.d.). *Django documentation*. Retrieved *[date]*, from https://docs.djangoproject.com/
- Russell, S., & Norvig, P. (2021). *Artificial intelligence: A modern approach* (4th ed.). Pearson.

## Appendix

*[Full code listing of the `ai/` module only (it's short and it's yours); for the rest, the repository URL is the listing. Include the link.]*
