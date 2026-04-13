"""Uniform Cost Search (UCS) - finds the cheapest path.

UCS keeps expanding the cheapest node so far. Since all moves cost the same here,
it ends up finding the shortest path like BFS, but in a more general way.
Used with a priority queue (min-heap).
"""

import heapq
from environment.maze_env import MazeEnv
from utils.evaluator import SearchResult, Timer


def ucs(env: MazeEnv) -> SearchResult:
    """Uniform Cost Search using a priority queue."""
    # get the start position and goal we need to reach
    start = env.get_start()
    goal  = env.get_goal()

    # use counter to break ties in the heap (otherwise would be comparing nodes which fails)
    counter = 0
    # heap stores (cost, counter, state, path, actions) - ordered by cost
    heap = [(0.0, counter, start, [start], [])]
    # track best cost to reach each state - need this for optimality
    best = {start: 0.0}
    expanded = 0
    generated = 1

    result = None
    with Timer() as t:
        while heap:
            # always pop the cheapest node first - thats UCS
            g, _, state, path, actions = heapq.heappop(heap)
            expanded += 1

            # skip if we already found a better way to this state
            # this is lazy deletion - avoids removing from heap
            if g > best.get(state, float('inf')):
                continue

            # check if we reached the goal
            if env.is_goal(state):
                # found it! build the result
                result = SearchResult(
                    algorithm_name  = "UCS",
                    path_found      = True,
                    path            = path,
                    actions         = actions,
                    path_length     = len(path) - 1,
                    path_cost       = g,
                    nodes_expanded  = expanded,
                    nodes_generated = generated,
                    execution_time_ms = 0.0,
                )
                break

            # explore all neighbors from current state
            for next_state, action, step_cost in env.get_successors(state):
                # calculate new cost to next_state if we go through current state
                new_g = g + step_cost
                # only add to heap if this is a better path than before
                if new_g < best.get(next_state, float('inf')):
                    best[next_state] = new_g
                    counter += 1
                    generated += 1
                    # push to heap with new cost
                    heapq.heappush(heap, (new_g, counter, next_state,
                                          path + [next_state], actions + [action]))

        # if we never found the goal
        if result is None:
            result = SearchResult(
                algorithm_name="UCS",
                path_found=False,
                nodes_expanded=expanded,
                nodes_generated=generated,
                execution_time_ms=0.0,
            )

    # set the execution time
    result.execution_time_ms = t.elapsed
    return result
