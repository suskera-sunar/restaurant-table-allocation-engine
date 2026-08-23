"""The frontier-loop search skeleton.

This is the loop from https://learn.kevalabs.com/ai/how-search-algorithms-work/
BFS is implemented for you as the worked example. DFS, greedy best-first, and
A* differ ONLY in take() -- implementing them is your work (the guide tells
you how; each is 1-4 lines).

Run this file directly to check your work:  python ai/search.py
"""


def search(start, is_goal, neighbors, take, h=None):
    """The one loop. Returns (goal_state, path, cost) or None.

    neighbors(state) -> list of (next_state, step_cost)
    take(frontier, h) -> remove and return one entry from the frontier
    h(state)          -> heuristic guess of cost-to-goal (greedy / A* only)

    Each frontier entry is a tuple: (state, path_so_far, cost_so_far).
    """
    frontier = [(start, [start], 0)]
    visited = set()

    while frontier:
        state, path, cost = take(frontier, h)   # <- THE question: which one next?
        if is_goal(state):
            return state, path, cost
        if state in visited:
            continue
        visited.add(state)
        for nxt, step_cost in neighbors(state):
            if nxt not in visited:
                frontier.append((nxt, path + [nxt], cost + step_cost))

    return None   # frontier empty: no solution exists


# --------------------------------------------------------------- take() zoo

def take_bfs(frontier, h=None):
    """Breadth-first: take the OLDEST entry (queue). Worked example."""
    return frontier.pop(0)


def take_dfs(frontier, h=None):
    """Depth-first: take the NEWEST entry (stack).

    TODO: one line. Which index does .pop() use for the newest?
    """
    raise NotImplementedError("take_dfs: your turn")


def take_greedy(frontier, h=None):
    """Greedy best-first: take the entry whose STATE has the smallest h.

    TODO: find the entry with minimal h(state), remove it from the
    frontier, and return it. (min() with a key function, or a loop --
    entry[0] is the state.)
    """
    raise NotImplementedError("take_greedy: your turn")


def take_astar(frontier, h=None):
    """A*: take the entry with the smallest f = cost_so_far + h(state).

    TODO: like take_greedy, but rank by entry[2] + h(entry[0]).
    """
    raise NotImplementedError("take_astar: your turn")


# ------------------------------------------------------- cafe team only

def bfs_levels(steps, depends_on):
    """Prep batches for the cafe project.

    steps       -> list of step names, e.g. ["grill patty", "assemble", ...]
    depends_on  -> dict: step -> list of steps that must finish FIRST

    Returns a list of batches (lists): batch 0 = every step with no
    unfinished prerequisite, batch 1 = everything unlocked once batch 0
    is done, and so on. This is BFS's ring-by-ring exploration read as a
    schedule -- see the "dependency levels" part of the guide.

    TODO (cafe team): repeat until every step is placed:
      1. find all unplaced steps whose prerequisites are ALL already placed
      2. that set is the next batch; if it's empty but steps remain,
         the dependencies contain a cycle -> raise ValueError
    """
    raise NotImplementedError("bfs_levels: cafe team, your turn")


# ------------------------------------------------------------- self-test

if __name__ == "__main__":
    # The guide's little graph: A-B, A-C, B-D, C-E, D-F, E-F (all cost 1)
    GRAPH = {
        "A": ["B", "C"], "B": ["A", "D"], "C": ["A", "E"],
        "D": ["B", "F"], "E": ["C", "F"], "F": ["D", "E"],
    }
    unit = lambda s: [(n, 1) for n in GRAPH[s]]
    to_f = lambda s: s == "F"

    # A weighted diamond where the greedy trap is visible:
    #   S->A costs 1, A->G costs 5 (A *looks* close: h=1, but the road is dear)
    #   S->B costs 3, B->G costs 2 (cheapest overall: 5)
    WEIGHTED = {"S": [("A", 1), ("B", 3)], "A": [("G", 5)], "B": [("G", 2)], "G": []}
    H = {"S": 3, "A": 1, "B": 2, "G": 0}   # admissible: never overestimates
    to_g = lambda s: s == "G"

    def check(name, take, neighbors, is_goal, start, expect_path=None, expect_cost=None):
        try:
            state, path, cost = search(start, is_goal, neighbors, take, H.get)
            ok = (expect_path is None or path == expect_path) and \
                 (expect_cost is None or cost == expect_cost)
            print(f"  {name:12s} path={'-'.join(path):11s} cost={cost}  "
                  + ("PASS" if ok else f"FAIL (expected {expect_path}, cost {expect_cost})"))
        except NotImplementedError as e:
            print(f"  {name:12s} not implemented yet -- {e}")

    print("frontier-loop self-test")
    print("unit graph, A to F (BFS must find the 3-hop path):")
    check("bfs", take_bfs, unit, to_f, "A", expect_path=["A", "B", "D", "F"])
    check("dfs", take_dfs, unit, to_f, "A")   # any path is fine; DFS makes no promise
    print("weighted diamond, S to G (greedy gets fooled, A* must not):")
    check("greedy", take_greedy, WEIGHTED.get, to_g, "S", expect_path=["S", "A", "G"], expect_cost=6)
    check("astar", take_astar, WEIGHTED.get, to_g, "S", expect_path=["S", "B", "G"], expect_cost=5)
    print("cafe team -- prep batches:")
    try:
        batches = bfs_levels(
            ["dough", "sauce", "assemble pizza", "bake", "brew coffee"],
            {"assemble pizza": ["dough", "sauce"], "bake": ["assemble pizza"]},
        )
        expect = [sorted(b) for b in batches] == [
            ["brew coffee", "dough", "sauce"], ["assemble pizza"], ["bake"]]
        print(f"  bfs_levels   {batches}  " + ("PASS" if expect else "FAIL"))
    except NotImplementedError as e:
        print(f"  bfs_levels   not implemented yet -- {e}")
