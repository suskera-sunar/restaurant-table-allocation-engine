"""Backward-chaining engine (gym team).

This is the 15-line engine from
https://learn.kevalabs.com/ai/how-expert-systems-work/ -- the engine is
DONE and you should not need to change it. Your work is the RULES list:
replace the 3 starter rules with 10-15 real ones from a trainer's logic,
layered so they chain (intermediate concepts like "cardio focus" that no
member is ever asked about directly).

Run a scripted demo:      python ai/rules.py
Run the real interview:   python ai/rules.py --interview
"""

RULES = [
    # TODO (gym team): replace these starters with your real rule base.
    # Shape: {"then": conclusion, "if": [condition, condition, ...]}
    # A condition no rule concludes is a LEAF -> the engine asks the user.
    {"then": "plan: upper/lower split", "if": ["goal: strength", "level: advanced"]},
    {"then": "plan: full-body circuit", "if": ["cardio focus", "level: beginner"]},
    {"then": "cardio focus",            "if": ["goal: weight loss", "3+ days a week"]},
]


def prove(goal, facts, denied, ask):
    """Can `goal` be established? Backward chaining = DFS over the proof tree."""
    if goal in facts:
        return True
    if goal in denied:
        return False
    rules = [r for r in RULES if r["then"] == goal]
    for rule in rules:                                     # OR: any rule will do
        if all(prove(c, facts, denied, ask) for c in rule["if"]):   # AND: all conditions
            facts.add(goal)
            return True
    if not rules:                                          # a leaf: ask the user
        if ask(goal):
            facts.add(goal)
            return True
    denied.add(goal)
    return False


def recommend(ask):
    """Try every plan-concluding rule in order; first proven wins."""
    facts, denied = set(), set()
    for rule in RULES:
        if rule["then"].startswith("plan") and prove(rule["then"], facts, denied, ask):
            return rule["then"], facts
    return None, facts


if __name__ == "__main__":
    import sys

    if "--interview" in sys.argv:
        ask = lambda q: input(f"{q}? (y/n) ").strip().lower() == "y"
    else:
        # Scripted member for the demo: weight-loss beginner, 3+ days a week
        SCRIPT = {
            "goal: strength": False,
            "goal: weight loss": True,
            "3+ days a week": True,
            "level: beginner": True,
            "level: advanced": False,
        }
        def ask(q):
            answer = SCRIPT.get(q, False)
            print(f"  asked: {q}? -> {'y' if answer else 'n'}")
            return answer
        print("scripted demo (use --interview for the real thing)")

    plan, facts = recommend(ask)
    if plan:
        print(f"recommendation: {plan}")
        print(f"facts established along the way: {sorted(facts)}")
    else:
        print("no plan matches -- refer to a trainer")
