"""Results storage and display.

Keeps track of how well each algorithm performed - path length, nodes looked at,
and how long it took to run.
"""

from dataclasses import dataclass, field
import time


@dataclass
class SearchResult:
    algorithm_name: str
    path_found: bool
    path: list = field(default_factory=list)
    actions: list = field(default_factory=list)
    path_length: int = 0
    path_cost: float = 0.0
    nodes_expanded: int = 0
    nodes_generated: int = 0
    execution_time_ms: float = 0.0

    def summary(self) -> str:
        status = "SUCCESS" if self.path_found else "FAILED "
        return (
            f"[{status}] {self.algorithm_name:<30} | "
            f"Path len: {self.path_length:>3} | "
            f"Cost: {self.path_cost:>6.1f} | "
            f"Expanded: {self.nodes_expanded:>5} | "
            f"Generated: {self.nodes_generated:>5} | "
            f"Time: {self.execution_time_ms:>7.3f} ms"
        )


class Timer:
    """Simple context-manager stopwatch."""
    # use this to measure how long an algorithm takes

    def __enter__(self):
        # start timing
        self.elapsed = 0.0
        self._start = time.perf_counter()
        return self

    def __exit__(self, *_):
        # stop timing and convert to milliseconds
        self.elapsed = (time.perf_counter() - self._start) * 1000


def print_results_table(results):
    """Pretty-prints a comparison table to stdout."""
    # show all the results in a nice table format
    print("\n" + "=" * 95)
    print(f"{'ALGORITHM':<30} | {'FOUND':>6} | {'PATH':>5} | {'COST':>6} | "
          f"{'EXPANDED':>8} | {'GENERATED':>9} | {'TIME (ms)':>9}")
    print("-" * 95)
    for r in results:
        # check if path was found
        found = "Yes" if r.path_found else "No"
        # show path length if successful
        path  = str(r.path_length) if r.path_found else "-"
        # show cost if successful
        cost  = f"{r.path_cost:.1f}" if r.path_found else "-"
        print(
            f"{r.algorithm_name:<30} | {found:>6} | {path:>5} | {cost:>6} | "
            f"{r.nodes_expanded:>8} | {r.nodes_generated:>9} | {r.execution_time_ms:>9.3f}"
        )
    print("=" * 95)
