"""
astar.py — A* Search
----------------------
Strategy  : Expand the node with lowest f(n) = g(n) + h(n).
            g(n) = cost from start to n.
            h(n) = heuristic estimate of cost from n to goal.
Data structure: Min-heap keyed on f(n).
Optimal?  : YES — provided h(n) is ADMISSIBLE (never overestimates).
Complete? : YES.
Key insight: A* balances exploration (g) and exploitation (h).
             With h=0 it degenerates to UCS; with h=perfect it expands
             only nodes on the optimal path.
"""

import heapq
from typing import Callable, Dict
from environment.maze_env import MazeEnv
from utils.evaluator import SearchResult, Timer


def astar(
    env: MazeEnv,
    heuristic: Callable[[int, int, MazeEnv], float],
    heuristic_name: str = "heuristic",
) -> SearchResult:
    """
    A* Search.

    Parameters
    ----------
    env            : MazeEnv instance
    heuristic      : function(state, goal, env) -> float  (must be admissible)
    heuristic_name : label shown in results table
    """
    start = env.get_start()
    goal  = env.get_goal()

    h0 = heuristic(start, goal, env)

    # Heap entries: (f, tie_breaker, state, g, path, actions)
    counter = 0
    heap = [(h0, counter, start, 0.0, [start], [])]

    best_g: Dict[int, float] = {start: 0.0}

    nodes_expanded  = 0
    nodes_generated = 1

    with Timer() as t:
        while heap:
            f, _, state, g, path, actions = heapq.heappop(heap)
            nodes_expanded += 1

            # Lazy deletion
            if g > best_g.get(state, float('inf')):
                continue

            if env.is_goal(state):
                return SearchResult(
                    algorithm_name  = f"A* ({heuristic_name})",
                    path_found      = True,
                    path            = path,
                    actions         = actions,
                    path_length     = len(path) - 1,
                    path_cost       = g,
                    nodes_expanded  = nodes_expanded,
                    nodes_generated = nodes_generated,
                    execution_time_ms = t.elapsed,
                )

            for next_state, action, step_cost in env.get_successors(state):
                new_g = g + step_cost
                if new_g < best_g.get(next_state, float('inf')):
                    best_g[next_state] = new_g
                    h = heuristic(next_state, goal, env)
                    f_new = new_g + h
                    counter += 1
                    nodes_generated += 1
                    heapq.heappush(heap, (f_new, counter, next_state, new_g,
                                          path + [next_state], actions + [action]))

    return SearchResult(
        algorithm_name  = f"A* ({heuristic_name})",
        path_found      = False,
        nodes_expanded  = nodes_expanded,
        nodes_generated = nodes_generated,
        execution_time_ms = t.elapsed,
    )
