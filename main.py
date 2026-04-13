"""
main.py — Entry point for the Maze-Solving Intelligent Agent project.
Runs BFS, DFS, UCS, and A* (Manhattan + Euclidean) on two maze sizes,
prints results tables, shows ASCII paths, and saves PNG charts.

Usage:
    python main.py
"""

import sys
import os

# Make sure sub-packages resolve correctly when run from the project root
sys.path.insert(0, os.path.dirname(__file__))

from environment.maze_env import MazeEnv, ACTION_NAMES
from algorithms import bfs, dfs, ucs, astar
from utils.heuristics import manhattan_distance, euclidean_distance
from utils.evaluator import SearchResult, print_results_table
from utils.visualizer import print_maze, save_maze_image, save_metrics_chart


# Maze definitions

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
    results = []

    results.append(bfs(env))
    results.append(dfs(env))
    results.append(ucs(env))
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

        # Build environment
        if maze_cfg["custom_map"]:
            env = MazeEnv(custom_map=maze_cfg["custom_map"])
        else:
            env = MazeEnv(map_name=maze_cfg["map_name"])

        print(f"\n  Grid size : {env.nrows} x {env.ncols}")
        print(f"  Start     : state {env.get_start()} "
              f"(row={env.state_to_coords(env.get_start())[0]}, "
              f"col={env.state_to_coords(env.get_start())[1]})")
        print(f"  Goal      : state {env.get_goal()} "
              f"(row={env.state_to_coords(env.get_goal())[0]}, "
              f"col={env.state_to_coords(env.get_goal())[1]})")

        # Show empty maze
        print_maze(env, title="Empty Maze")

        # Run algorithms
        results = run_all_algorithms(env)

        # Results table
        print_results_table(results)

        # Show ASCII path for each algorithm
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
