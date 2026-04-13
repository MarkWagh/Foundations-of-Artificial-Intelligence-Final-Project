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
    # grab start and goal from maze env
    start = env.get_start()
    goal = env.get_goal()

    # use a stack for DFS - pop from end gives us depth-first behavior
    # store (current pos, path taken, actions taken)
    stk = [(start, [start], [])]
    # track visited to avoid cycles
    seen = {start}

    # need to count how many nodes we expanded and generated
    expanded = 0
    generated = 1

    result = None
    timer = Timer()
    
    with timer:
        while stk:
            # pop from stack - this gives LIFO (depth first)
            pos, path, moves = stk.pop()
            expanded += 1

            # did we reach the goal?
            if env.is_goal(pos):
                # yes! make result object
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

            # reversed so we explore left branches first (more natural ordering)
            for neighbor, direction, _ in reversed(env.get_successors(pos)):
                # only add if not already visited
                if neighbor not in seen:
                    seen.add(neighbor)
                    generated += 1
                    # push to stack for next iteration
                    stk.append((neighbor, path + [neighbor], moves + [direction]))

        # handle case where we never found the goal
        if result is None:
            result = SearchResult(
                algorithm_name="DFS",
                path_found=False,
                nodes_expanded=expanded,
                nodes_generated=generated,
                execution_time_ms=0.0,
            )

    # store the time
    result.execution_time_ms = timer.elapsed
    return result
