"""
bfs.py — Breadth-First Search
------------------------------
Strategy  : Expand shallowest (fewest hops) node first.
Data structure: FIFO queue.
Optimal?  : YES — for uniform step costs (all costs = 1 here).
Complete? : YES — will always find a solution if one exists.
Time/Space: O(b^d) where b=branching factor, d=solution depth.
"""

from collections import deque
from typing import Optional, List

from environment.maze_env import MazeEnv
from utils.evaluator import SearchResult, Timer


def bfs(env: MazeEnv) -> SearchResult:
    """
    Breadth-First Search on the MazeEnv state space.

    Returns a SearchResult with the shortest path (fewest steps).
    """
    start = env.get_start()
    goal  = env.get_goal()

    # Each entry in the queue: (current_state, path_so_far, actions_so_far)
    queue: deque = deque()
    queue.append((start, [start], []))

    # Visited set prevents re-expanding already-seen states
    visited = {start}

    nodes_expanded  = 0
    nodes_generated = 1  # start node

    with Timer() as t:
        while queue:
            state, path, actions = queue.popleft()
            nodes_expanded += 1

            if env.is_goal(state):
                return SearchResult(
                    algorithm_name  = "BFS",
                    path_found      = True,
                    path            = path,
                    actions         = actions,
                    path_length     = len(path) - 1,
                    path_cost       = float(len(path) - 1),
                    nodes_expanded  = nodes_expanded,
                    nodes_generated = nodes_generated,
                    execution_time_ms = t.elapsed,
                )

            for next_state, action, cost in env.get_successors(state):
                if next_state not in visited:
                    visited.add(next_state)
                    nodes_generated += 1
                    queue.append((next_state, path + [next_state], actions + [action]))

    # No path found
    return SearchResult(
        algorithm_name  = "BFS",
        path_found      = False,
        nodes_expanded  = nodes_expanded,
        nodes_generated = nodes_generated,
        execution_time_ms = t.elapsed,
    )
