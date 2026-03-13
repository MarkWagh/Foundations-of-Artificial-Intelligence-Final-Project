"""
core/state.py
-------------
SearchNode encapsulates all information needed by search algorithms:
current position, parent pointer, action taken, path cost, and depth.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Tuple


@dataclass
class SearchNode:
    """
    A node in the search tree.

    Attributes
    ----------
    state      : (row, col) position in the maze.
    parent     : Parent SearchNode, or None for the root.
    action     : Direction string that led to this node.
    path_cost  : Cumulative cost g(n) from root to this node.
    depth      : Depth of this node in the search tree.
    heuristic  : Heuristic value h(n) (0 for uninformed search).
    """

    state     : Tuple[int, int]
    parent    : Optional[SearchNode] = field(default=None, repr=False)
    action    : Optional[str]        = None
    path_cost : float                = 0.0
    depth     : int                  = 0
    heuristic : float                = 0.0

    # f(n) = g(n) + h(n) — used as priority for A* and UCS
    @property
    def f(self) -> float:
        return self.path_cost + self.heuristic

    # Allow nodes to be compared by f-value in a priority queue
    def __lt__(self, other: SearchNode) -> bool:
        return self.f < other.f

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SearchNode):
            return NotImplemented
        return self.state == other.state

    def __hash__(self) -> int:
        return hash(self.state)

    # ------------------------------------------------------------------
    # Path reconstruction
    # ------------------------------------------------------------------

    def extract_path(self) -> list[Tuple[int, int]]:
        """Walk parent pointers and return ordered list of positions."""
        path, node = [], self
        while node is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path

    def extract_actions(self) -> list[str]:
        """Return ordered list of actions (directions) from root to this node."""
        actions, node = [], self
        while node.parent is not None:
            actions.append(node.action)
            node = node.parent
        actions.reverse()
        return actions
