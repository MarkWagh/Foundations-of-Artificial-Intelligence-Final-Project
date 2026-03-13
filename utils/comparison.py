"""
utils/comparison.py
-------------------
Run all four algorithms on the same maze and produce a side-by-side
comparison table with analysis notes.
"""

from __future__ import annotations
from typing import List

from maze_solver.core.maze            import Maze
from maze_solver.core.result          import SearchResult
from maze_solver.algorithms.bfs       import bfs
from maze_solver.algorithms.dfs       import dfs
from maze_solver.algorithms.ucs       import ucs
from maze_solver.algorithms.astar     import astar
from maze_solver.utils.heuristics     import manhattan, euclidean


def run_all(maze: Maze) -> List[SearchResult]:
    """
    Execute BFS, DFS, UCS, A*(Manhattan), and A*(Euclidean) on *maze*.

    Returns
    -------
    List[SearchResult]
        One result per algorithm, in the order listed above.
    """
    return [
        bfs(maze),
        dfs(maze),
        ucs(maze),
        astar(maze, heuristic=manhattan),
        astar(maze, heuristic=euclidean),
    ]


def print_comparison(results: List[SearchResult]) -> None:
    """Print a formatted comparison table to stdout."""
    col_w = 22
    headers = [
        "Algorithm", "Solved", "Path len", "Path cost",
        "Expanded", "Generated", "Max frontier", "Time (ms)",
    ]

    # Header row
    print("\n" + "=" * (col_w * len(headers)))
    print("ALGORITHM COMPARISON")
    print("=" * (col_w * len(headers)))
    header_line = "".join(h.ljust(col_w) for h in headers)
    print(header_line)
    print("-" * (col_w * len(headers)))

    for r in results:
        row = [
            r.algorithm,
            "✓" if r.solved else "✗",
            str(r.path_length),
            f"{r.path_cost:.1f}",
            str(r.nodes_expanded),
            str(r.nodes_generated),
            str(r.max_frontier),
            f"{r.execution_time * 1000:.3f}",
        ]
        print("".join(cell.ljust(col_w) for cell in row))

    print("=" * (col_w * len(headers)))
    _print_analysis(results)


def _print_analysis(results: List[SearchResult]) -> None:
    """Print qualitative analysis notes based on the results."""
    solved = [r for r in results if r.solved]
    if not solved:
        print("\n[!] No algorithm found a solution. Check maze connectivity.")
        return

    min_path = min(r.path_length for r in solved)
    min_exp  = min(r.nodes_expanded for r in solved)
    fastest  = min(solved, key=lambda r: r.execution_time)

    print("\nANALYSIS NOTES")
    print("-" * 50)

    for r in solved:
        notes = []
        if r.path_length == min_path:
            notes.append("optimal path length")
        if r.nodes_expanded == min_exp:
            notes.append("fewest nodes expanded")
        if r is fastest:
            notes.append("fastest execution")
        tag = f"  ← {', '.join(notes)}" if notes else ""
        print(f"  {r.algorithm:<28}{tag}")

    print()
