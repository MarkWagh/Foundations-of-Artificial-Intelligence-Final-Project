"""Different guesses for how far away the goal is.

Used by A* to guide the search smarter. Manhattan and Euclidean distances
both work well on grid mazes and never overestimate the real distance.
"""

import math
from environment.maze_env import MazeEnv


def manhattan_distance(state: int, goal: int, env: MazeEnv) -> float:
    """Manhattan distance - sum of row and column differences."""
    r1, c1 = env.state_to_coords(state)
    r2, c2 = env.state_to_coords(goal)
    return abs(r1 - r2) + abs(c1 - c2)


def euclidean_distance(state: int, goal: int, env: MazeEnv) -> float:
    """Straight-line distance as the crow flies."""
    r1, c1 = env.state_to_coords(state)
    r2, c2 = env.state_to_coords(goal)
    return math.sqrt((r1 - r2) ** 2 + (c1 - c2) ** 2)
