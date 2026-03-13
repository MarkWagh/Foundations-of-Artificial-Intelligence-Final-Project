"""
tests/test_algorithms.py
------------------------
Unit tests for all four search algorithms and supporting modules.
Run with:  python -m pytest tests/ -v
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from maze_solver.core.maze        import Maze
from maze_solver.core.state       import SearchNode
from maze_solver.algorithms.bfs   import bfs
from maze_solver.algorithms.dfs   import dfs
from maze_solver.algorithms.ucs   import ucs
from maze_solver.algorithms.astar import astar
from maze_solver.utils.heuristics import manhattan, euclidean, zero


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

SIMPLE_MAZE = """\
S..
.#.
..G
"""

# Start and Goal are separated by a full wall — truly no path
BLOCKED_MAZE = """\
S##
###
##G
"""


@pytest.fixture
def simple():
    return Maze.from_string(SIMPLE_MAZE)


@pytest.fixture
def blocked():
    return Maze.from_string(BLOCKED_MAZE)


@pytest.fixture
def random_maze():
    return Maze.generate_random(10, 10, wall_density=0.25, seed=7)


# ------------------------------------------------------------------
# Maze construction tests
# ------------------------------------------------------------------

class TestMaze:
    def test_dimensions(self, simple):
        assert simple.rows == 3
        assert simple.cols == 3

    def test_start_goal(self, simple):
        assert simple.start == (0, 0)
        assert simple.goal  == (2, 2)

    def test_wall_placement(self, simple):
        from maze_solver.core.maze import WALL
        assert simple.grid[1][1] == WALL

    def test_invalid_cell(self, simple):
        with pytest.raises(IndexError):
            simple.set_wall(99, 99)

    def test_wall_on_start_raises(self, simple):
        with pytest.raises(ValueError):
            simple.set_wall(0, 0)

    def test_random_generation(self, random_maze):
        assert random_maze.rows == 10
        assert random_maze.cols == 10
        # Must always be solvable
        result = bfs(random_maze)
        assert result.solved

    def test_neighbors(self, simple):
        # (0,0) in a 3×3 maze with wall at (1,1)
        neighbors = dict(
            (state, label) for state, label, _ in simple.get_neighbors(0, 0)
        )
        # Should have DOWN → (1,0) and RIGHT → (0,1)
        assert (1, 0) in neighbors
        assert (0, 1) in neighbors
        # Should NOT include out-of-bounds or walls
        assert (0, -1) not in neighbors


# ------------------------------------------------------------------
# Search node tests
# ------------------------------------------------------------------

class TestSearchNode:
    def test_path_extraction(self):
        root  = SearchNode((0, 0))
        child = SearchNode((0, 1), parent=root, action="RIGHT", path_cost=1.0, depth=1)
        grand = SearchNode((0, 2), parent=child, action="RIGHT", path_cost=2.0, depth=2)

        assert grand.extract_path()    == [(0, 0), (0, 1), (0, 2)]
        assert grand.extract_actions() == ["RIGHT", "RIGHT"]

    def test_f_value(self):
        node = SearchNode((3, 4), path_cost=5.0, heuristic=3.0)
        assert node.f == 8.0

    def test_ordering(self):
        a = SearchNode((0, 0), path_cost=2.0, heuristic=1.0)  # f=3
        b = SearchNode((1, 1), path_cost=5.0, heuristic=0.0)  # f=5
        assert a < b


# ------------------------------------------------------------------
# BFS tests
# ------------------------------------------------------------------

class TestBFS:
    def test_solves_simple(self, simple):
        r = bfs(simple)
        assert r.solved
        assert r.path[0]  == simple.start
        assert r.path[-1] == simple.goal

    def test_no_solution(self, blocked):
        assert not bfs(blocked).solved

    def test_optimal_path_length(self, simple):
        # Simple 3×3 with center wall: S(0,0)→(1,0)→(2,0)→(2,1)→G(2,2) = 4 steps
        r = bfs(simple)
        assert r.path_length == 4

    def test_metrics_populated(self, simple):
        r = bfs(simple)
        assert r.nodes_expanded  > 0
        assert r.nodes_generated > 0
        assert r.execution_time  > 0


# ------------------------------------------------------------------
# DFS tests
# ------------------------------------------------------------------

class TestDFS:
    def test_solves_simple(self, simple):
        r = dfs(simple)
        assert r.solved
        assert r.path[0]  == simple.start
        assert r.path[-1] == simple.goal

    def test_no_solution(self, blocked):
        assert not dfs(blocked).solved

    def test_path_valid(self, random_maze):
        r = dfs(random_maze)
        if r.solved:
            # Every consecutive pair must be neighbours
            for i in range(len(r.path) - 1):
                a, b = r.path[i], r.path[i + 1]
                assert abs(a[0]-b[0]) + abs(a[1]-b[1]) == 1


# ------------------------------------------------------------------
# UCS tests
# ------------------------------------------------------------------

class TestUCS:
    def test_solves_simple(self, simple):
        r = ucs(simple)
        assert r.solved

    def test_optimal(self, simple):
        # UCS and BFS must agree on cost for uniform grids
        r_ucs = ucs(simple)
        r_bfs = bfs(simple)
        assert r_ucs.path_cost == r_bfs.path_cost

    def test_no_solution(self, blocked):
        assert not ucs(blocked).solved


# ------------------------------------------------------------------
# A* tests
# ------------------------------------------------------------------

class TestAStar:
    def test_solves_simple_manhattan(self, simple):
        r = astar(simple, heuristic=manhattan)
        assert r.solved
        assert r.path[-1] == simple.goal

    def test_solves_simple_euclidean(self, simple):
        r = astar(simple, heuristic=euclidean)
        assert r.solved

    def test_optimal_agrees_with_bfs(self, random_maze):
        r_astar = astar(random_maze, heuristic=manhattan)
        r_bfs   = bfs(random_maze)
        assert r_astar.solved == r_bfs.solved
        if r_astar.solved:
            assert r_astar.path_cost == r_bfs.path_cost

    def test_astar_expands_fewer_than_bfs(self, random_maze):
        r_astar = astar(random_maze, heuristic=manhattan)
        r_bfs   = bfs(random_maze)
        if r_astar.solved and r_bfs.solved:
            # A* should generally expand ≤ BFS nodes with Manhattan heuristic
            assert r_astar.nodes_expanded <= r_bfs.nodes_expanded

    def test_zero_heuristic_equals_ucs(self, random_maze):
        r_astar_zero = astar(random_maze, heuristic=zero)
        r_ucs_       = ucs(random_maze)
        if r_astar_zero.solved and r_ucs_.solved:
            assert r_astar_zero.path_cost == r_ucs_.path_cost

    def test_no_solution(self, blocked):
        assert not astar(blocked, heuristic=manhattan).solved


# ------------------------------------------------------------------
# Heuristic tests
# ------------------------------------------------------------------

class TestHeuristics:
    def test_manhattan_same_cell(self):
        assert manhattan((3, 4), (3, 4)) == 0

    def test_manhattan_value(self):
        assert manhattan((0, 0), (3, 4)) == 7

    def test_euclidean_value(self):
        import math
        assert abs(euclidean((0, 0), (3, 4)) - 5.0) < 1e-9

    def test_admissibility_manhattan(self, random_maze):
        """
        Manhattan distance must never overestimate the true cost.
        Verify for every cell that h(n) ≤ actual BFS distance.
        """
        from collections import deque
        # BFS from goal to compute true distances
        goal     = random_maze.goal
        dist     = {goal: 0}
        queue    = deque([goal])
        while queue:
            r, c = queue.popleft()
            for (nr, nc), _, _ in random_maze.get_neighbors(r, c):
                if (nr, nc) not in dist:
                    dist[(nr, nc)] = dist[(r, c)] + 1
                    queue.append((nr, nc))

        for (r, c), true_dist in dist.items():
            h = manhattan((r, c), goal)
            assert h <= true_dist, (
                f"Manhattan heuristic {h} > true dist {true_dist} at ({r},{c})"
            )
