"""Maze solver entry point. Runs all algorithms on various test mazes."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from environment.maze_env import MazeEnv, ACTION_NAMES
from algorithms import bfs, dfs, ucs, astar
from utils.heuristics import manhattan_distance, euclidean_distance
from utils.evaluator import SearchResult, print_results_table
from utils.visualizer import print_maze, save_maze_image, save_metrics_chart

MAPS = {
    "4x4 Standard": {
        "map_name": "4x4",
        "custom_map": None,
    },
    "8x8 Standard": {
        "map_name": "8x8",
        "custom_map": None,
    },
    "Custom 6x6": {
        "map_name": None,
        "custom_map": [
            "SFFFFF",
            "FHFFFH",
            "FFFHFF",
            "FHFFFF",
            "FFFHFF",
            "FFFFFG",
        ],
    },
    "20x20 Standard": {
        "map_name": None,
        "custom_map": [
            "SFFHFFFHFFFHFFFHFFFF",
            "FHFFFHFFFHFFFHFFFHFF",
            "FFFHFFFHFFFHFFFHFFFH",
            "FHFFFHFFFHFFFHFFFHFF",
            "FFFHFFFHFFFHFFFHFFFH",
            "FHFFFHFFFHFFFHFFFHFF",
            "FFFHFFFHFFFHFFFHFFFH",
            "FHFFFHFFFHFFFHFFFHFF",
            "FFFHFFFHFFFHFFFHFFFH",
            "FHFFFHFFFHFFFHFFFHFF",
            "FFFHFFFHFFFHFFFHFFFH",
            "FHFFFHFFFHFFFHFFFHFF",
            "FFFHFFFHFFFHFFFHFFFH",
            "FHFFFHFFFHFFFHFFFHFF",
            "FFFHFFFHFFFHFFFHFFFH",
            "FHFFFHFFFHFFFHFFFHFF",
            "FFFHFFFHFFFHFFFHFFFH",
            "FHFFFHFFFHFFFHFFFHFF",
            "FFFHFFFHFFFHFFFHFFFH",
            "FHFFFHFFFHFFFHFFFHFG",
        ],
    },
}


def run_all_algorithms(env: MazeEnv) -> list:
    """Runs all 5 algorithms on the maze and returns their results."""
    # test each algorithm to see how they perform
    results = []

    # try each one
    results.append(bfs(env))
    results.append(dfs(env))
    results.append(ucs(env))
    # A* with both heuristics to compare
    results.append(astar(env, manhattan_distance, heuristic_name="Manhattan"))
    results.append(astar(env, euclidean_distance, heuristic_name="Euclidean"))

    return results


def print_path_steps(result: SearchResult, env: MazeEnv) -> None:
    """Shows the moves the algorithm made to reach the goal."""
    if not result.path_found:
        print(f"  {result.algorithm_name}: No path found.\n")
        return
    moves = [ACTION_NAMES[a] for a in result.actions]
    print(f"  {result.algorithm_name} path ({result.path_length} steps): "
          + " -> ".join(moves) + "\n")


def main():
    output_dir = os.path.join(os.path.dirname(__file__), "results")

    for maze_label, maze_cfg in MAPS.items():
        print("\n" + "#" * 70)
        print(f"  MAZE: {maze_label}")
        print("#" * 70)

        # create the maze environment from config
        if maze_cfg["custom_map"]:
            env = MazeEnv(custom_map=maze_cfg["custom_map"])
        else:
            env = MazeEnv(map_name=maze_cfg["map_name"])

        # show info about this maze
        print(f"\n  Grid size : {env.nrows} x {env.ncols}")
        print(f"  Start     : state {env.get_start()} "
              f"(row={env.state_to_coords(env.get_start())[0]}, "
              f"col={env.state_to_coords(env.get_start())[1]})")
        print(f"  Goal      : state {env.get_goal()} "
              f"(row={env.state_to_coords(env.get_goal())[0]}, "
              f"col={env.state_to_coords(env.get_goal())[1]})")

        # show what the empty maze looks like
        print_maze(env, title="Empty Maze")

        # run all search algorithms on this maze
        results = run_all_algorithms(env)

        # print results in table format
        print_results_table(results)

        # show the actual paths taken
        print("\n  --- Path Visualisations (ASCII) ---")
        for res in results:
            if res.path_found:
                print_maze(env, path=res.path, title=f"{res.algorithm_name} Path")
            print_path_steps(res, env)

        # Save PNG charts
        safe_label = maze_label.replace(" ", "_")
        maze_out   = os.path.join(output_dir, safe_label)
        save_maze_image(env, results, output_dir=maze_out)
        save_metrics_chart(results, output_dir=maze_out)

    print("\n  All experiments complete.")
    print(f"  Charts saved to: {output_dir}\n")


if __name__ == "__main__":
    main()
