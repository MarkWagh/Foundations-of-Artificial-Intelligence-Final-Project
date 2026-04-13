"""Draws the maze and makes charts comparing the algorithms.

Shows ASCII grid with paths marked, and generates PNG images
with side-by-side performance comparisons.
"""

import os
from typing import List, Optional
import numpy as np

ASCII_TILES = {b'S': 'S', b'G': 'G', b'F': '.', b'H': '#'}

COLOUR_MAP = {
    b'S': [0.2, 0.8, 0.2],
    b'G': [1.0, 0.6, 0.0],
    b'F': [0.95, 0.95, 1.0],
    b'H': [0.15, 0.15, 0.15],
}
PATH_COLOUR = [0.4, 0.6, 1.0]


def print_maze(env, path=None, title=""):
    path_set = set(path) if path else set()
    start, goal = env.get_start(), env.get_goal()
    if title:
        print(f"\n  {title}")
    border = "+" + "-" * (env.ncols * 2 + 1) + "+"
    print(border)
    for r in range(env.nrows):
        row_str = "| "
        for c in range(env.ncols):
            state = env.coords_to_state(r, c)
            tile  = env.desc[r][c]
            if state == start:
                ch = 'S'
            elif state == goal:
                ch = 'G'
            elif state in path_set:
                ch = '*'
            else:
                ch = ASCII_TILES.get(tile, '?')
            row_str += ch + " "
        print(row_str + "|")
    print(border)
    print("  S=Start  G=Goal  #=Hole  .=Open  *=Path\n")


def save_maze_image(env, results, output_dir="results"):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("[Visualizer] matplotlib not installed — skipping PNG output.")
        return

    os.makedirs(output_dir, exist_ok=True)
    n = len(results)

    def base_grid():
        grid = np.zeros((env.nrows, env.ncols, 3))
        for r in range(env.nrows):
            for c in range(env.ncols):
                grid[r, c] = COLOUR_MAP.get(env.desc[r][c], [1, 1, 1])
        return grid

    cols = min(n, 3)
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))
    axes = np.array(axes).flatten()

    for i, res in enumerate(results):
        ax = axes[i]
        grid = base_grid()
        if res.path_found:
            for state in res.path:
                r, c = env.state_to_coords(state)
                if env.desc[r][c] not in (b'S', b'G'):
                    grid[r, c] = PATH_COLOUR
        ax.imshow(grid, interpolation='nearest')
        _annotate(ax, env, res.path if res.path_found else [])
        status = "" if res.path_found else " [NO PATH]"
        ax.set_title(
            f"{res.algorithm_name}{status}\n"
            f"Steps={res.path_length}  Expanded={res.nodes_expanded}  "
            f"{res.execution_time_ms:.2f}ms",
            fontsize=8,
        )
        ax.axis('off')

    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle("Search Algorithm Comparison", fontsize=13, fontweight='bold')
    fig.tight_layout()
    path_out = os.path.join(output_dir, "comparison.png")
    fig.savefig(path_out, bbox_inches='tight', dpi=130)
    plt.close(fig)
    print(f"[Visualizer] Saved comparison  -> {path_out}")


def save_metrics_chart(results, output_dir: str = "results") -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        return

    os.makedirs(output_dir, exist_ok=True)
    names    = [r.algorithm_name      for r in results]
    expanded = [r.nodes_expanded      for r in results]
    lengths  = [r.path_length         for r in results]
    times    = [r.execution_time_ms   for r in results]

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    axes[0].bar(names, expanded, color='steelblue');  axes[0].set_title("Nodes Expanded");      axes[0].tick_params(axis='x', rotation=20)
    axes[1].bar(names, lengths,  color='seagreen');   axes[1].set_title("Path Length (steps)"); axes[1].tick_params(axis='x', rotation=20)
    axes[2].bar(names, times,    color='tomato');     axes[2].set_title("Execution Time (ms)"); axes[2].tick_params(axis='x', rotation=20)
    fig.suptitle("Algorithm Performance Metrics", fontsize=13, fontweight='bold')
    fig.tight_layout()
    p = os.path.join(output_dir, "metrics.png")
    fig.savefig(p, bbox_inches='tight', dpi=130)
    plt.close(fig)
    print(f"[Visualizer] Saved metrics     -> {p}")


def _annotate(ax, env, path: List[int]) -> None:
    sr, sc = env.state_to_coords(env.get_start())
    gr, gc = env.state_to_coords(env.get_goal())
    ax.text(sc, sr, 'S', ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    ax.text(gc, gr, 'G', ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    for state in path[1:-1]:
        r, c = env.state_to_coords(state)
        ax.text(c, r, 'o', ha='center', va='center', fontsize=7, color='navy')
    for r in range(env.nrows + 1):
        ax.axhline(r - 0.5, color='grey', linewidth=0.4)
    for c in range(env.ncols + 1):
        ax.axvline(c - 0.5, color='grey', linewidth=0.4)
