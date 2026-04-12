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

# Install dependencies
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

*BFS is optimal for uniform-cost mazes (all step costs = 1).

## Maze Test Cases

The program runs experiments on four maze sizes:

1. **4×4 Standard** — Small maze from Gymnasium (quick validation)
2. **8×8 Standard** — Medium maze from Gymnasium (balanced performance)
3. **Custom 6×6** — Custom-designed maze with strategic obstacles
4. **20×20 Standard** — Large maze for clear performance differentiation

### Output Metrics
For each maze, the program generates:
- **ASCII path visualizations** — Printed to console
- **Comparison PNG** — Side-by-side paths for all algorithms
- **Metrics PNG** — Bar charts showing:
  - Nodes Expanded
  - Path Length (steps)
  - Execution Time (ms)

## Key Features

✅ **State-space search modeling** — Treats maze as state transition system
✅ **Multiple heuristics** — A* with Manhattan and Euclidean distances
✅ **Performance profiling** — Tracks nodes expanded, path cost, execution time
✅ **Visual comparison** — Matplotlib charts and ASCII visualizations
✅ **Pure Python implementation** — No external AI frameworks

## Files & Responsibilities

### Core Algorithm Files
- `algorithms/bfs.py` — Returns SearchResult with shortest path
- `algorithms/dfs.py` — Returns SearchResult with first path found
- `algorithms/ucs.py` — Returns SearchResult with lowest-cost path
- `algorithms/astar.py` — Returns SearchResult optimized by heuristic

### Utilities
- `utils/evaluator.py` — SearchResult dataclass, Timer context manager
- `utils/visualizer.py` — ASCII printing, PNG generation
- `utils/comparison.py` — Run all algorithms, produce comparison table
- `utils/heuristics.py` — Manhattan and Euclidean distance functions

### Configuration
- `environment/maze_env.py` — Gymnasium MazeEnv wrapper
  - `get_start()` / `get_goal()` — Query maze endpoints
  - `get_successors(state)` — Get valid next states
  - `is_goal(state)` — Check if goal reached
  - `state_to_coords()` / `coords_to_state()` — Coordinate conversion

## Missing / Future Enhancements

⚠️ **Items not yet implemented:**
- [ ] Unit tests in `tests/test_algorithms.py` — Currently empty; needs algorithm validation tests
- [ ] Bidirectional search algorithm
- [ ] IDA* (Iterative Deepening A*)
- [ ] Greedy Best-First Search
- [ ] Memory profiling for large mazes (>50×50)
- [ ] Interactive visualization (live path exploration)
- [ ] Custom maze editor/loader from file
- [ ] Comparison with other maze-solving libraries
- [ ] Performance benchmarks across maze sizes
- [ ] Obstacle course generation (procedural mazes)
- [ ] Grid world with multiple goals or rewards

## Usage Examples

### Run All Experiments
```bash
python main.py
```
This runs BFS, DFS, UCS, and A* on all four maze sizes, printing ASCII paths and generating PNG charts.

### Test a Single Algorithm
```bash
from environment.maze_env import MazeEnv
from algorithms.bfs import bfs

env = MazeEnv(map_name="8x8")
result = bfs(env)
print(f"Path length: {result.path_length}")
print(f"Nodes expanded: {result.nodes_expanded}")
print(f"Time: {result.execution_time_ms:.3f}ms")
```

### Compare All Algorithms
```bash
from utils.comparison import run_all, print_comparison
from environment.maze_env import MazeEnv

env = MazeEnv(custom_map=my_custom_map)
results = run_all(env)
print_comparison(results)
```

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
