"""DFS (Depth-First Search) algorithm.

Explores deep into the maze before backtracking.
Usually faster than BFS but doesn't find shortest paths.
Uses iteration instead of recursion for large mazes.
"""

from environment.maze_env import MazeEnv
from utils.evaluator import SearchResult, Timer


def dfs(env: MazeEnv) -> SearchResult:
    """Find a path using depth-first search.
    
    Goes as far down each branch as possible.
    May find longer paths but uses less memory than BFS.
    """
    start = env.get_start()
    goal = env.get_goal()

    # Stack holds (position, path taken, actions taken)
    stk = [(start, [start], [])]
    seen = {start}

    expanded = 0
    generated = 1

    result = None
    timer = Timer()
    
    with timer:
        while stk:
            pos, path, moves = stk.pop()
            expanded += 1

            if env.is_goal(pos):
                result = SearchResult(
                    algorithm_name="DFS",
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

            # Add neighbors in reverse so left paths explored first
            for neighbor, direction, _ in reversed(env.get_successors(pos)):
                if neighbor not in seen:
                    seen.add(neighbor)
                    generated += 1
                    stk.append((neighbor, path + [neighbor], moves + [direction]))

        if result is None:
            result = SearchResult(
                algorithm_name="DFS",
                path_found=False,
                nodes_expanded=expanded,
                nodes_generated=generated,
                execution_time_ms=0.0,
            )

    result.execution_time_ms = timer.elapsed
    return result
