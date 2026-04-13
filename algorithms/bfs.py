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
    # get starting and goal positions from the maze
    start = env.get_start()
    goal = env.get_goal()

    # use queue for BFS - need FIFO so we explore layer by layer
    # each item has (position, path so far, moves taken)
    q = deque([(start, [start], [])])
    # keep track of visited nodes so we don't revisit them
    seen = {start}

    # counters for the stats we need to report
    expanded = 0
    generated = 1

    result = None
    timer = Timer()
    
    with timer:
        while q:
            # pop from front of queue - thats the BFS part
            pos, path, moves = q.popleft()
            expanded += 1

            # check if we found the goal position
            if env.is_goal(pos):
                # build result when we found it
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

            # get all neighbors we can move to from current position
            for neighbor, direction, step_cost in env.get_successors(pos):
                # only explore if we havent visited this state
                if neighbor not in seen:
                    seen.add(neighbor)
                    generated += 1
                    # add to queue - this ensures breadth-first ordering
                    q.append((neighbor, path + [neighbor], moves + [direction]))

        # if no path found, still need to report failed result
        if result is None:
            result = SearchResult(
                algorithm_name="BFS",
                path_found=False,
                nodes_expanded=expanded,
                nodes_generated=generated,
                execution_time_ms=0.0,
            )

    # calculate elapsed time now that we exited the timer context
    result.execution_time_ms = timer.elapsed
    return result
