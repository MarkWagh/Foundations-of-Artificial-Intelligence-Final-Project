"""maze_solver — Intelligent Maze-Solving Agent"""
from maze_solver.core.maze            import Maze
from maze_solver.core.result          import SearchResult
from maze_solver.algorithms.bfs       import bfs
from maze_solver.algorithms.dfs       import dfs
from maze_solver.algorithms.ucs       import ucs
from maze_solver.algorithms.astar     import astar
from maze_solver.utils.heuristics     import manhattan, euclidean
from maze_solver.utils.comparison     import run_all, print_comparison
from maze_solver.utils.visualizer     import print_result, plot_comparison

__all__ = [
    "Maze", "SearchResult",
    "bfs", "dfs", "ucs", "astar",
    "manhattan", "euclidean",
    "run_all", "print_comparison",
    "print_result", "plot_comparison",
]
