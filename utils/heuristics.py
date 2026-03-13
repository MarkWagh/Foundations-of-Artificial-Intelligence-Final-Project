"""
heuristics.py
-------------
Admissible heuristic functions for informed search (A*).

Both heuristics are ADMISSIBLE for the FrozenLake maze because they
never overestimate the true shortest-path distance (step cost = 1).

  - Manhattan distance: exact or under-estimate on grid mazes.
  - Euclidean distance: always <= Manhattan distance, so also admissible.
"""

import math
from environment.maze_env import MazeEnv


def manhattan_distance(state: int, goal: int, env: MazeEnv) -> float:
    """
    |Δrow| + |Δcol|  — the classic grid heuristic.

    Admissible because each move changes row OR col by exactly 1,
    so the true cost is always >= manhattan distance.
    """
    r1, c1 = env.state_to_coords(state)
    r2, c2 = env.state_to_coords(goal)
    return abs(r1 - r2) + abs(c1 - c2)


def euclidean_distance(state: int, goal: int, env: MazeEnv) -> float:
    """
    sqrt(Δrow^2 + Δcol^2) — straight-line distance.

    Admissible because Euclidean <= Manhattan for any grid.
    Less informed than Manhattan but still guides search toward goal.
    """
    r1, c1 = env.state_to_coords(state)
    r2, c2 = env.state_to_coords(goal)
    return math.sqrt((r1 - r2) ** 2 + (c1 - c2) ** 2)


def zero_heuristic(state: int, goal: int, env: MazeEnv) -> float:
    """h(n) = 0 — makes A* behave like UCS. Useful baseline."""
    return 0.0


# Registry — makes it easy to iterate in experiments
HEURISTICS = {
    "Manhattan": manhattan_distance,
    "Euclidean": euclidean_distance,
    "Zero (UCS baseline)": zero_heuristic,
}
