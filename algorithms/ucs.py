"""
ucs.py — Uniform Cost Search
------------------------------
Strategy  : Expand the node with the lowest cumulative path cost g(n).
Data structure: Min-heap (priority queue) keyed on g(n).
Optimal?  : YES — always finds the minimum-cost path.
Complete? : YES.
Relation  : Equivalent to Dijkstra's algorithm on a graph.
            Also equivalent to A* with h(n) = 0.
"""

import heapq
from typing import Dict
from environment.maze_env import MazeEnv
from utils.evaluator import SearchResult, Timer


def ucs(env: MazeEnv) -> SearchResult:
    """
    Uniform Cost Search.
    Priority queue entries: (cumulative_cost, tie_breaker, state, path, actions)
    """
    start = env.get_start()
    goal  = env.get_goal()

    # (g_cost, counter, state, path, actions)
    counter = 0
    heap = [(0.0, counter, start, [start], [])]

    # Best known cost to reach each state
    best_cost: Dict[int, float] = {start: 0.0}

    nodes_expanded  = 0
    nodes_generated = 1

    with Timer() as t:
        while heap:
            g, _, state, path, actions = heapq.heappop(heap)
            nodes_expanded += 1

            # Lazy deletion: skip if we already found a cheaper route
            if g > best_cost.get(state, float('inf')):
                continue

            if env.is_goal(state):
                return SearchResult(
                    algorithm_name  = "UCS",
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
                if new_g < best_cost.get(next_state, float('inf')):
                    best_cost[next_state] = new_g
                    counter += 1
                    nodes_generated += 1
                    heapq.heappush(heap, (new_g, counter, next_state,
                                          path + [next_state], actions + [action]))

    return SearchResult(
        algorithm_name  = "UCS",
        path_found      = False,
        nodes_expanded  = nodes_expanded,
        nodes_generated = nodes_generated,
        execution_time_ms = t.elapsed,
    )
