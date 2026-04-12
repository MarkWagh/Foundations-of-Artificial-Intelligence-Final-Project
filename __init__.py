"""maze_solver — Intelligent Maze-Solving Agent"""
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.ucs import ucs
from algorithms.astar import astar
from utils.heuristics import manhattan_distance, euclidean_distance
from utils.evaluator import SearchResult

__all__ = [
    "bfs", "dfs", "ucs", "astar",
    "manhattan_distance", "euclidean_distance",
    "SearchResult",
]
