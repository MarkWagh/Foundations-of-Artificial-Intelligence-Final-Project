"""
dfs.py — Depth-First Search
-----------------------------
Strategy  : Expand deepest node first.
Data structure: LIFO stack (or recursion).
Optimal?  : NO — may find a long or winding path.
Complete? : NO — can loop without a visited set; complete WITH visited set
            but may still miss shorter paths.
Time/Space: O(b^m) time, O(bm) space, m=max depth.

Note: We use an explicit stack (iterative DFS) to avoid Python's recursion
limit on large mazes.
"""

from typing import List
from environment.maze_env import MazeEnv
from utils.evaluator import SearchResult, Timer


def dfs(env: MazeEnv) -> SearchResult:
    """
    Iterative Depth-First Search.
    Returns the FIRST path found (not necessarily shortest).
    """
    start = env.get_start()
    goal  = env.get_goal()

    # Stack entries: (state, path, actions)
    stack: List = [(start, [start], [])]
    visited = {start}

    nodes_expanded  = 0
    nodes_generated = 1

    result = None
    with Timer() as t:
        while stack:
            state, path, actions = stack.pop()   # LIFO
            nodes_expanded += 1

            if env.is_goal(state):
                result = SearchResult(
                    algorithm_name  = "DFS",
                    path_found      = True,
                    path            = path,
                    actions         = actions,
                    path_length     = len(path) - 1,
                    path_cost       = float(len(path) - 1),
                    nodes_expanded  = nodes_expanded,
                    nodes_generated = nodes_generated,
                    execution_time_ms = 0.0,
                )
                break

            # Push successors in reverse order so left-most is explored first
            for next_state, action, cost in reversed(env.get_successors(state)):
                if next_state not in visited:
                    visited.add(next_state)
                    nodes_generated += 1
                    stack.append((next_state, path + [next_state], actions + [action]))

        if result is None:
            result = SearchResult(
                algorithm_name  = "DFS",
                path_found      = False,
                nodes_expanded  = nodes_expanded,
                nodes_generated = nodes_generated,
                execution_time_ms = 0.0,
            )

    result.execution_time_ms = t.elapsed
    return result
