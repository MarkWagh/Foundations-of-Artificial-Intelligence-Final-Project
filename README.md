# Maze-Solving Intelligent Agent
### Final Project — AI Search Algorithms

Uses OpenAI Gymnasium's `FrozenLake-v1` as the maze environment.

## Project Structure
```
maze_solver/
├── main.py                  # Entry point — run all experiments
├── algorithms/
│   ├── __init__.py
│   ├── bfs.py               # Breadth-First Search
│   ├── dfs.py               # Depth-First Search
│   ├── ucs.py               # Uniform Cost Search
│   └── astar.py             # A* Search
├── environment/
│   ├── __init__.py
│   └── maze_env.py          # Gymnasium wrapper + state-space model
├── utils/
│   ├── __init__.py
│   ├── heuristics.py        # Manhattan & Euclidean distance heuristics
│   ├── visualizer.py        # ASCII + matplotlib maze visualizations
│   └── evaluator.py         # Metrics: path length, nodes expanded, time
└── results/                 # Output charts and reports saved here
```

## Setup
```bash
pip install gymnasium matplotlib numpy
python main.py
```

## Algorithms
| Algorithm | Optimal? | Complete? | Uses Heuristic? |
|-----------|----------|-----------|-----------------|
| BFS       | Yes*     | Yes       | No              |
| DFS       | No       | No        | No              |
| UCS       | Yes      | Yes       | No              |
| A*        | Yes      | Yes       | Yes             |

*BFS is optimal for uniform-cost mazes.
