"""
core/result.py
--------------
SearchResult is a plain data container returned by every algorithm.
It bundles the solution path together with performance metrics so that
the comparison module can work with a uniform interface.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class SearchResult:
    """
    Outcome of a single search run.

    Attributes
    ----------
    algorithm        : Name of the algorithm (e.g. "A*").
    solved           : True if a path from start to goal was found.
    path             : Ordered list of (row, col) cells in the solution.
    actions          : Ordered list of direction strings.
    path_length      : Number of steps in the solution (0 if unsolved).
    nodes_expanded   : How many nodes were popped from the frontier.
    nodes_generated  : How many nodes were added to the frontier.
    max_frontier     : Peak size of the frontier during the search.
    execution_time   : Wall-clock seconds consumed by the algorithm.
    path_cost        : Total cumulative cost of the solution path.
    """

    algorithm       : str
    solved          : bool
    path            : List[Tuple[int, int]] = field(default_factory=list)
    actions         : List[str]             = field(default_factory=list)
    path_length     : int                   = 0
    nodes_expanded  : int                   = 0
    nodes_generated : int                   = 0
    max_frontier    : int                   = 0
    execution_time  : float                 = 0.0
    path_cost       : float                 = 0.0

    # ------------------------------------------------------------------
    # Convenience
    # ------------------------------------------------------------------

    def summary(self) -> str:
        status = "✓ Solved" if self.solved else "✗ No solution"
        lines  = [
            f"Algorithm       : {self.algorithm}",
            f"Status          : {status}",
            f"Path length     : {self.path_length} steps",
            f"Path cost       : {self.path_cost:.2f}",
            f"Nodes expanded  : {self.nodes_expanded}",
            f"Nodes generated : {self.nodes_generated}",
            f"Max frontier    : {self.max_frontier}",
            f"Execution time  : {self.execution_time * 1000:.4f} ms",
        ]
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "algorithm"      : self.algorithm,
            "solved"         : self.solved,
            "path_length"    : self.path_length,
            "path_cost"      : round(self.path_cost, 4),
            "nodes_expanded" : self.nodes_expanded,
            "nodes_generated": self.nodes_generated,
            "max_frontier"   : self.max_frontier,
            "execution_time_ms": round(self.execution_time * 1000, 4),
        }
