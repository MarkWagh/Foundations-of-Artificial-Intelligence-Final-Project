"""
maze_env.py
-----------
Wraps Gymnasium's FrozenLake-v1 into a clean state-space search interface.

State  : integer index (row * ncols + col)
Actions: 0=LEFT, 1=DOWN, 2=RIGHT, 3=UP
"""

import gymnasium as gym
import numpy as np
from typing import List, Tuple, Dict


# Human-readable action labels
ACTION_NAMES = {0: "LEFT", 1: "DOWN", 2: "RIGHT", 3: "UP"}

# Movement deltas for (row, col) — matches Gymnasium's action encoding
ACTION_DELTAS = {
    0: (0, -1),   # LEFT
    1: (1,  0),   # DOWN
    2: (0,  1),   # RIGHT
    3: (-1, 0),   # UP
}

# Tile types
TILE_START = b'S'
TILE_GOAL  = b'G'
TILE_FROZEN = b'F'
TILE_HOLE  = b'H'


class MazeEnv:
    """
    A deterministic, state-space search wrapper around FrozenLake-v1.

    Provides:
      - get_start() / get_goal()
      - get_successors(state) -> list of (next_state, action, cost)
      - is_goal(state)
      - state_to_coords(state) / coords_to_state(row, col)
      - The raw grid (desc) for visualisation
    """

    def __init__(self, map_name: str = "4x4", custom_map: List[str] = None):
        """
        Parameters
        ----------
        map_name    : "4x4" or "8x8" (ignored when custom_map is given)
        custom_map  : optional list of strings, e.g. ["SFFF", "FHFH", ...]
        """
        if custom_map:
            desc = [list(row.encode()) for row in custom_map]
            self._gym_env = gym.make(
                "FrozenLake-v1",
                desc=custom_map,
                is_slippery=False,
                render_mode=None,
            )
        else:
            self._gym_env = gym.make(
                "FrozenLake-v1",
                map_name=map_name,
                is_slippery=False,
                render_mode=None,
            )

        self.desc: np.ndarray = self._gym_env.unwrapped.desc   # 2-D byte array
        self.nrows: int = self.desc.shape[0]
        self.ncols: int = self.desc.shape[1]
        self.n_states: int = self.nrows * self.ncols

        self._start: int = self._find_tile(TILE_START)
        self._goal:  int = self._find_tile(TILE_GOAL)

    # ------------------------------------------------------------------
    # Core interface used by every search algorithm
    # ------------------------------------------------------------------

    def get_start(self) -> int:
        return self._start

    def get_goal(self) -> int:
        return self._goal

    def is_goal(self, state: int) -> bool:
        return state == self._goal

    def is_valid(self, state: int) -> bool:
        """Returns False for hole tiles."""
        row, col = self.state_to_coords(state)
        return self.desc[row][col] != TILE_HOLE

    def get_successors(self, state: int) -> List[Tuple[int, int, float]]:
        """
        Returns a list of (next_state, action, step_cost) tuples.
        Holes and out-of-bound cells are excluded.
        Step cost is always 1.0 (uniform cost maze).
        """
        row, col = self.state_to_coords(state)
        successors = []

        for action, (dr, dc) in ACTION_DELTAS.items():
            new_row, new_col = row + dr, col + dc

            # Boundary check
            if not (0 <= new_row < self.nrows and 0 <= new_col < self.ncols):
                continue

            next_state = self.coords_to_state(new_row, new_col)

            # Skip holes
            if not self.is_valid(next_state):
                continue

            successors.append((next_state, action, 1.0))

        return successors

    # ------------------------------------------------------------------
    # Coordinate helpers
    # ------------------------------------------------------------------

    def state_to_coords(self, state: int) -> Tuple[int, int]:
        return divmod(state, self.ncols)

    def coords_to_state(self, row: int, col: int) -> int:
        return row * self.ncols + col

    def get_tile(self, state: int) -> bytes:
        row, col = self.state_to_coords(state)
        return self.desc[row][col]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _find_tile(self, tile_type: bytes) -> int:
        for r in range(self.nrows):
            for c in range(self.ncols):
                if self.desc[r][c] == tile_type:
                    return self.coords_to_state(r, c)
        raise ValueError(f"Tile '{tile_type}' not found in map.")

    def __repr__(self) -> str:
        return f"MazeEnv({self.nrows}x{self.ncols}, start={self._start}, goal={self._goal})"
