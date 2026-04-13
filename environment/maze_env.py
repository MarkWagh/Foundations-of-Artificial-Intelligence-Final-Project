"""Maze environment wrapper.

Wraps FrozenLake and turns it into a state-space search problem.
Provides access to start, goal, successors, etc.
"""

import gymnasium as gym
import numpy as np


ACTION_NAMES = {0: "LEFT", 1: "DOWN", 2: "RIGHT", 3: "UP"}
# deltas for each action - tells us how row/col change
ACTION_DELTAS = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}
TILE_START = b'S'
TILE_GOAL = b'G'
TILE_FROZEN = b'F'
# holes are walls we cant go through
TILE_HOLE = b'H'


class MazeEnv:
    """Wraps FrozenLake into a search problem.
    
    Gives us methods to get the start and goal, and to find what states
    we can reach from each current state.
    """

    def __init__(self, map_name="4x4", custom_map=None):
        """Create a maze from a standard name or custom grid.
        
        map_name: "4x4" or "8x8" (standard Gymnasium mazes)
        custom_map: list of strings like ["SFFF", "FHFF", ...] (S=start, G=goal, F=free, H=hole)
        """
        # use custom map if provided, otherwise use standard one
        if custom_map:
            desc = [list(row.encode()) for row in custom_map]
            self._gym_env = gym.make(
                "FrozenLake-v1",
                desc=custom_map,
                is_slippery=False,
                render_mode=None,
            )
        else:
            # load standard gymnasium maze
            self._gym_env = gym.make(
                "FrozenLake-v1",
                map_name=map_name,
                is_slippery=False,
                render_mode=None,
            )

        # extract the maze description
        self.desc = self._gym_env.unwrapped.desc
        self.nrows = self.desc.shape[0]
        self.ncols = self.desc.shape[1]
        self.n_states = self.nrows * self.ncols

        self._start = self._find_tile(TILE_START)
        self._goal = self._find_tile(TILE_GOAL)

    def get_start(self):
        # starting position in the maze
        return self._start
    def get_goal(self):
        # where we need to reach
        return self._goal
    def is_goal(self, state):
        # check if we reached the goal
        return state == self._goal
    def is_valid(self, state):
        """Returns False for hole tiles."""
        # need to make sure we can actually go there
        row, col = self.state_to_coords(state)
        return self.desc[row][col] != TILE_HOLE

    def get_successors(self, state):
        """Returns list of (next_state, action, cost) - excludes holes and boundaries."""
        # find all valid moves from current position
        row, col = self.state_to_coords(state)
        successors = []

        # try all 4 directions
        for action, (dr, dc) in ACTION_DELTAS.items():
            new_row, new_col = row + dr, col + dc

            # make sure we're still in bounds
            if not (0 <= new_row < self.nrows and 0 <= new_col < self.ncols):
                continue

            next_state = self.coords_to_state(new_row, new_col)

            # dont allow going through holes
            if not self.is_valid(next_state):
                continue

            # add this as a valid move
            successors.append((next_state, action, 1.0))

        return successors
    def state_to_coords(self, state):
        # convert single number to row,col position
        return divmod(state, self.ncols)

    def coords_to_state(self, row, col):
        # convert row,col to single number
        return row * self.ncols + col
    def get_tile(self, state):
        # what type of tile is at this state
        row, col = self.state_to_coords(state)
        return self.desc[row][col]
    def _find_tile(self, tile_type):
        for r in range(self.nrows):
            for c in range(self.ncols):
                if self.desc[r][c] == tile_type:
                    return self.coords_to_state(r, c)
        raise ValueError(f"Tile '{tile_type}' not found in map.")

    def __repr__(self):
        return f"MazeEnv({self.nrows}x{self.ncols}, start={self._start}, goal={self._goal})"
