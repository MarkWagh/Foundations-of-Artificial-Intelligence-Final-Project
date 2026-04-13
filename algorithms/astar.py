"""A* Search - the best of both worlds.

A* combines the actual cost from start (g) with an educated guess to the goal (h).
It's like Dijkstra's algorithm but with a heuristic to guide the search.
If the heuristic is good, A* is much faster than UCS.
"""

import heapq
from environment.maze_env import MazeEnv
from utils.evaluator import SearchResult, Timer


def astar(
    env: MazeEnv,
    heuristic,
    heuristic_name: str = "heuristic",
) -> SearchResult:
    """A* Search with a given heuristic function."""
    # get start position and where we wanna go
    start = env.get_start()
    goal  = env.get_goal()

    # calculate initial heuristic estimate from start to goal
    h0 = heuristic(start, goal, env)

    # counter prevents comparison errors in heap (cant compare nodes)
    counter = 0
    # heap stores (f_score, counter, state, g, path, actions)
    # f_score = g + h = priority in A*
    heap = [(h0, counter, start, 0.0, [start], [])]
    # track best g value we found for each state
    best_g = {start: 0.0}
    expanded = 0
    generated = 1

    result = None
    with Timer() as t:
        while heap:
            # pop the node with best f score (most promising one)
            f, _, state, g, path, actions = heapq.heappop(heap)
            expanded += 1

            # skip if we already found cheaper route to this node
            if g > best_g.get(state, float('inf')):
                continue

            # are we at the goal?
            if env.is_goal(state):
                # nice! we found it
                result = SearchResult(
                    algorithm_name  = f"A* ({heuristic_name})",
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

            # explore all neighbors from this state
            for next_state, action, step_cost in env.get_successors(state):
                # cost to reach next_state going through current state  
                new_g = g + step_cost
                # only process if this is better than before
                if new_g < best_g.get(next_state, float('inf')):
                    best_g[next_state] = new_g
                    # compute heuristic estimate for this node
                    h = heuristic(next_state, goal, env)
                    # f = g + h is the priority
                    f_new = new_g + h
                    counter += 1
                    generated += 1
                    # add to heap
                    heapq.heappush(heap, (f_new, counter, next_state, new_g,
                                          path + [next_state], actions + [action]))

        if result is None:
            result = SearchResult(
                algorithm_name=f"A* ({heuristic_name})",
                path_found=False,
                nodes_expanded=expanded,
                nodes_generated=generated,
                execution_time_ms=0.0,
            )

    result.execution_time_ms = t.elapsed
    return result
