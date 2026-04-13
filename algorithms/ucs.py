"""Uniform Cost Search (UCS) - finds the cheapest path.

UCS keeps expanding the cheapest node so far. Since all moves cost the same here,
it ends up finding the shortest path like BFS, but in a more general way.
Used with a priority queue (min-heap).
"""

import heapq
from typing import Dict
from environment.maze_env import MazeEnv
from utils.evaluator import SearchResult, Timer


def ucs(env: MazeEnv) -> SearchResult:
    """Uniform Cost Search using a priority queue."""
    start = env.get_start()
    goal  = env.get_goal()

    # Heap stores (cost, tiebreaker, state, path, moves)
    counter = 0
    heap = [(0.0, counter, start, [start], [])]
    best = {start: 0.0}
    expanded = 0
    generated = 1

    result = None
    with Timer() as t:
        while heap:
            g, _, state, path, actions = heapq.heappop(heap)
            expanded += 1

            # Skip if we found a better route to this state already
            if g > best.get(state, float('inf')):
                continue

            if env.is_goal(state):
                result = SearchResult(
                    algorithm_name  = "UCS",
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
                if new_g < best.get(next_state, float('inf')):
                    best[next_state] = new_g
                    counter += 1
                    generated += 1
                    heapq.heappush(heap, (new_g, counter, next_state,
                                          path + [next_state], actions + [action]))

        if result is None:
            result = SearchResult(
                algorithm_name  = "UCS",
                path_found      = False,
                nodes_expanded  = expanded,
                nodes_generated = generated,
                execution_time_ms = 0.0,
            )

    result.execution_time_ms = t.elapsed
    return result
