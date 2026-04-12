# Maze-Solving Intelligent Agent
### Final Project — CS 5100 Foundations of AI

Classical AI search algorithms applied to maze navigation using OpenAI Gymnasium's `FrozenLake-v1` environment.

## Project Structure
```
maze-solver/
├── __init__.py
├── main.py                          # Entry point — runs all experiments
├── README.md                        # Project documentation
│
├── algorithms/                      # Search algorithm implementations
│   ├── __init__.py
│   ├── bfs.py                       # Breadth-First Search
│   ├── dfs.py                       # Depth-First Search
│   ├── ucs.py                       # Uniform Cost Search
│   └── astar.py                     # A* Search (Manhattan & Euclidean)
│
├── core/                            # Core data structures
│   ├── __init__.py
│   ├── maze.py                      # Maze environment model
│   ├── state.py                     # State representation (if used)
│   └── result.py                    # SearchResult dataclass (deprecated — see evaluator.py)
│
├── environment/                     # Gymnasium wrapper
│   ├── __init__.py
│   └── maze_env.py                  # MazeEnv class — state-space interface
│
├── utils/                           # Utilities & visualization
│   ├── __init__.py
│   ├── comparison.py                # run_all() function + print_comparison()
│   ├── evaluator.py                 # SearchResult dataclass, Timer, metrics
│   ├── heuristics.py                # Manhattan & Euclidean distance heuristics
│   └── visualizer.py                # ASCII visualization + matplotlib charts
│
├── tests/                           # Unit tests
│   ├── __init__.py
│   └── test_algorithms.py           # Algorithm validation tests
│
├── results/                         # Generated output (charts, reports)
│   ├── 4x4_Standard/
│   │   ├── comparison.png           # Side-by-side path visualizations
│   │   └── metrics.png              # Performance metrics bar charts
│   ├── 8x8_Standard/
│   │   ├── comparison.png
│   │   └── metrics.png
│   ├── Custom_6x6/
│   │   ├── comparison.png
│   │   └── metrics.png
│   └── 20x20_Standard/
│       ├── comparison.png
│       └── metrics.png
│
└── maze-venv/                       # Python virtual environment
    ├── bin/                         # Executables (python, pip, etc.)
    ├── include/
    ├── lib/                         # Site-packages (dependencies)
    └── pyvenv.cfg
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation
```bash
# Create virtual environment
python3 -m venv maze-venv

# Activate virtual environment
source maze-venv/bin/activate

# Install dependencies these are important
pip install gymnasium matplotlib numpy

# Run experiments
python main.py
```

## Algorithms Implemented

| Algorithm | Optimal? | Complete? | Uses Heuristic? | Search Strategy |
|-----------|----------|-----------|-----------------|-----------------|
| **BFS**   | Yes*     | Yes       | No              | Explore shallowest nodes first (FIFO) |
| **DFS**   | No       | No        | No              | Explore deepest nodes first (LIFO) |
| **UCS**   | Yes      | Yes       | No              | Explore lowest-cost nodes first (Dijkstra) |
| **A***    | Yes      | Yes       | Yes             | Minimize f(n) = g(n) + h(n) |


### Output Metrics
For each maze, the program generates:
- **ASCII path visualizations** — Printed to console
- **Comparison PNG** — Side-by-side paths for all algorithms
- **Metrics PNG** — Bar charts showing:
  - Nodes Expanded
  - Path Length (steps)
  - Execution Time (ms)



## Usage Examples

### Run All Experiments
```bash
python main.py
```
This runs BFS, DFS, UCS, and A* on all four maze sizes, printing ASCII paths and generating PNG charts.


## Results & Performance

See `results/` folder for generated visualizations. Each maze size shows:
- **Small mazes (4×4, 6×6)** — All algorithms fast (<0.1ms), differences minimal
- **Medium maze (8×8)** — Execution time ~0.02ms, path optimization visible
- **Large maze (20×20)** — Execution time ~0.5ms, clear algorithm differentiation
  - DFS: fastest but suboptimal paths
  - BFS/UCS: optimal but more expensive
  - A*: balanced with heuristic guidance

## Dependencies

- `gymnasium` — FrozenLake environment
- `matplotlib` — PNG chart generation
- `numpy` — Numerical operations

Install with: `pip install gymnasium matplotlib numpy`

## Notes

- All algorithms are **deterministic** (no stochastic behavior)
- Mazes use **uniform cost** (all moves cost 1)
- No diagonal movement (4-directional: LEFT, DOWN, RIGHT, UP)
- Heuristics are **admissible** (never overestimate true cost)
