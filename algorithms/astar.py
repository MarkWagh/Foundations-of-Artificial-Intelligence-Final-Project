"""A* Search - the best of both worlds.

A* combines the actual cost from start (g) with an educated guess to the goal (h).
It's like Dijkstra's algorithm but with a heuristic to guide the search.
If the heuristic is good, A* is much faster than UCS.
"""

import heapq
from typing import Callable, Dict
from environment.maze_env import MazeEnv
from utils.evaluator import SearchResult, Timer


def astar(
    env: MazeEnv,
    heuristic,
    heuristic_name: str = "heuristic",
) -> SearchResult:
    """A* Search with a given heuristic function."""
    start = env.get_start()
    goal  = env.get_goal()

    h0 = heuristic(start, goal, env)

    # Priority queue: (f_score, tiebreaker, state, actual_cost, path, moves)
    counter = 0
    heap = [(h0, counter, start, 0.0, [start], [])]
    best_g = {start: 0.0}
    expanded = 0
    generated = 1

    result = None
    with Timer() as t:
        while heap:
            f, _, state, g, path, actions = heapq.heappop(heap)
            expanded += 1

            # Already found a shorter route to this state
            if g > best_g.get(state, float('inf')):
                continue

            if env.is_goal(state):
                result = SearchResult(
                    algorithm_name  = f"A* ({heuristic_name})",
                    path_found      = True,
                    path            = path,
                    actions         = actions,
                    path_length     = len(path) - 1,
                    path_cost       = g,
                    nodes_expanded  = expanded,
                    nodes_generated = generated,
                    execution_time_ms = 0.0,
                )
                break

            for next_state, action, step_cost in env.get_successors(state):
                new_g = g + step_cost
                if new_g < best_g.get(next_state, float('inf')):
                    best_g[next_state] = new_g
                    h = heuristic(next_state, goal, env)
                    f_new = new_g + h
                    counter += 1
                    generated += 1
                    heapq.heappush(heap, (f_new, counter, next_state, new_g,
                                          path + [next_state], actions + [action]))

        if result is None:
            result = SearchResult(
                algorithm_name  = f"A* ({heuristic_name})",
                path_found      = False,
                nodes_expanded  = expanded,
                nodes_generated = generated,
                execution_time_ms = 0.0,
            )

    result.execution_time_ms = t.elapsed
    return result
