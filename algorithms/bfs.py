"""BFS (Breadth-First Search) algorithm.

Explores the maze level by level, guaranteeing shortest path.
Uses FIFO queue so we process nodes in the order discovered.
"""

from collections import deque
from environment.maze_env import MazeEnv
from utils.evaluator import SearchResult, Timer


def bfs(env: MazeEnv) -> SearchResult:
    """Find shortest maze path using breadth-first search.
    
    Explores all neighbors at distance d before distance d+1.
    Always finds the optimal solution for equal-cost moves.
    """
    start = env.get_start()
    goal = env.get_goal()

    # Queue holds: (current position, full path to here, moves made)
    q = deque([(start, [start], [])])
    seen = {start}

    expanded = 0
    generated = 1

    result = None
    timer = Timer()
    
    with timer:
        while q:
            pos, path, moves = q.popleft()
            expanded += 1

            # Reached the goal?
            if env.is_goal(pos):
                result = SearchResult(
                    algorithm_name="BFS",
                    path_found=True,
                    path=path,
                    actions=moves,
                    path_length=len(path) - 1,
                    path_cost=float(len(path) - 1),
                    nodes_expanded=expanded,
                    nodes_generated=generated,
                    execution_time_ms=0.0,
                )
                break

            # Explore each valid neighbor
            for neighbor, direction, step_cost in env.get_successors(pos):
                if neighbor not in seen:
                    seen.add(neighbor)
                    generated += 1
                    q.append((neighbor, path + [neighbor], moves + [direction]))

        if result is None:
            result = SearchResult(
                algorithm_name="BFS",
                path_found=False,
                nodes_expanded=expanded,
                nodes_generated=generated,
                execution_time_ms=0.0,
            )

    result.execution_time_ms = timer.elapsed
    return result
