"""
core/maze.py
------------
Defines the Maze environment: grid representation, obstacle placement,
start/goal locations, and neighbour generation for the search agents.
"""

import random
from typing import List, Tuple, Optional


EMPTY = 0
WALL  = 1
START = 2
GOAL  = 3

_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # up, down, left, right
_DIR_LABELS  = ["UP",   "DOWN", "LEFT",  "RIGHT"]


class Maze:
    """
    A 2-D grid maze.

    Attributes
    ----------
    rows, cols : int
        Dimensions of the grid.
    grid : List[List[int]]
        Cell values (EMPTY / WALL / START / GOAL).
    start : Tuple[int, int]
        (row, col) of the start cell.
    goal  : Tuple[int, int]
        (row, col) of the goal cell.
    """

    def __init__(self, rows: int, cols: int):
        if rows < 3 or cols < 3:
            raise ValueError("Maze must be at least 3×3.")
        self.rows  = rows
        self.cols  = cols
        self.grid  = [[EMPTY] * cols for _ in range(rows)]
        self.start = (0, 0)
        self.goal  = (rows - 1, cols - 1)

    # ------------------------------------------------------------------
    # Grid helpers
    # ------------------------------------------------------------------

    def is_valid(self, row: int, col: int) -> bool:
        """Return True if (row, col) is inside the grid bounds."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_walkable(self, row: int, col: int) -> bool:
        """Return True if the cell exists and is not a wall."""
        return self.is_valid(row, col) and self.grid[row][col] != WALL

    def set_wall(self, row: int, col: int) -> None:
        if not self.is_valid(row, col):
            raise IndexError(f"Cell ({row}, {col}) is outside the maze.")
        if (row, col) in (self.start, self.goal):
            raise ValueError("Cannot place a wall on start or goal.")
        self.grid[row][col] = WALL

    def set_start(self, row: int, col: int) -> None:
        if not self.is_valid(row, col):
            raise IndexError(f"Cell ({row}, {col}) is outside the maze.")
        # Clear old start
        sr, sc = self.start
        self.grid[sr][sc] = EMPTY
        self.start = (row, col)
        self.grid[row][col] = START

    def set_goal(self, row: int, col: int) -> None:
        if not self.is_valid(row, col):
            raise IndexError(f"Cell ({row}, {col}) is outside the maze.")
        # Clear old goal
        gr, gc = self.goal
        self.grid[gr][gc] = EMPTY
        self.goal = (row, col)
        self.grid[row][col] = GOAL

    # ------------------------------------------------------------------
    # Neighbour generation (used by every search algorithm)
    # ------------------------------------------------------------------

    def get_neighbors(
        self, row: int, col: int
    ) -> List[Tuple[Tuple[int, int], str, float]]:
        """
        Return walkable neighbours of (row, col).

        Returns
        -------
        List of (position, action_label, step_cost) triples.
        Step cost is always 1.0 for a uniform grid.
        """
        neighbors = []
        for (dr, dc), label in zip(_DIRECTIONS, _DIR_LABELS):
            nr, nc = row + dr, col + dc
            if self.is_walkable(nr, nc):
                neighbors.append(((nr, nc), label, 1.0))
        return neighbors

    # ------------------------------------------------------------------
    # Procedural generation
    # ------------------------------------------------------------------

    @classmethod
    def generate_random(
        cls,
        rows: int,
        cols: int,
        wall_density: float = 0.30,
        seed: Optional[int] = None,
    ) -> "Maze":
        """
        Generate a random maze using random wall placement.
        A BFS connectivity check ensures start→goal is reachable.

        Parameters
        ----------
        wall_density : float
            Fraction of interior cells to turn into walls (0.0 – 0.6).
        seed : int, optional
            Random seed for reproducibility.
        """
        if not 0.0 <= wall_density <= 0.6:
            raise ValueError("wall_density must be between 0.0 and 0.6.")

        rng = random.Random(seed)
        maze = cls(rows, cols)
        maze.set_start(0, 0)
        maze.set_goal(rows - 1, cols - 1)

        protected = {maze.start, maze.goal}

        for r in range(rows):
            for c in range(cols):
                if (r, c) not in protected:
                    if rng.random() < wall_density:
                        maze.grid[r][c] = WALL

        # Guarantee connectivity via BFS
        if not maze._is_connected():
            maze._carve_path(rng)

        return maze

    @classmethod
    def from_string(cls, layout: str) -> "Maze":
        """
        Build a maze from a multi-line string.

        Legend
        ------
        '#' → wall, ' ' or '.' → empty, 'S' → start, 'G' → goal
        """
        lines = [l for l in layout.strip().splitlines() if l]
        rows  = len(lines)
        cols  = max(len(l) for l in lines)
        maze  = cls(rows, cols)

        start_found = goal_found = False
        for r, line in enumerate(lines):
            for c, ch in enumerate(line.ljust(cols)):
                if ch == "#":
                    maze.grid[r][c] = WALL
                elif ch == "S":
                    maze.start = (r, c)
                    maze.grid[r][c] = START
                    start_found = True
                elif ch == "G":
                    maze.goal = (r, c)
                    maze.grid[r][c] = GOAL
                    goal_found = True

        if not start_found:
            raise ValueError("Maze string must contain exactly one 'S'.")
        if not goal_found:
            raise ValueError("Maze string must contain exactly one 'G'.")
        return maze

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _is_connected(self) -> bool:
        """BFS check: can we reach goal from start?"""
        from collections import deque
        visited = {self.start}
        queue   = deque([self.start])
        while queue:
            r, c = queue.popleft()
            if (r, c) == self.goal:
                return True
            for (nr, nc), _, _ in self.get_neighbors(r, c):
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return False

    def _carve_path(self, rng: random.Random) -> None:
        """Remove walls along a random walk from start to goal."""
        r, c = self.start
        gr, gc = self.goal
        while (r, c) != (gr, gc):
            dr = (1 if r < gr else -1) if r != gr else 0
            dc = (1 if c < gc else -1) if c != gc else 0
            # Randomly choose row or col movement
            if dr and dc:
                if rng.random() < 0.5:
                    dc = 0
                else:
                    dr = 0
            r, c = r + dr, c + dc
            if (r, c) not in {self.start, self.goal}:
                self.grid[r][c] = EMPTY

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        symbols = {EMPTY: "  ", WALL: "██", START: " S", GOAL: " G"}
        rows_str = []
        for r in range(self.rows):
            rows_str.append("".join(symbols[self.grid[r][c]] for c in range(self.cols)))
        return "\n".join(rows_str)
