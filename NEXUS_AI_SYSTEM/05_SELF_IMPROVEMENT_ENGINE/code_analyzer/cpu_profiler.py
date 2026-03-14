# --- NEXUS_AI_SYSTEM/05_SELF_IMPROVEMENT_ENGINE/code_analysis/cpu_profiler.py ---

import cProfile
import pstats
import io
from typing import Callable, Any

class CPUProfiler:
    """
    A wrapper around Python's built-in cProfile and pstats modules to
    programmatically profile function calls and identify CPU bottlenecks.

    This profiler helps in understanding:
    - Total number of function calls.
    - Time spent in each function.
    - Cumulative time spent in functions.
    - Call hierarchy and dependencies.
    """

    def __init__(self):
        self.profiler = cProfile.Profile()
        self.stats: pstats.Stats = None

    def profile_function(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """
        Profiles the execution of a single function call.

        Args:
            func (Callable): The function to profile.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            Any: The return value of the profiled function.
        """
        print(f"\n--- Profiling function: {func.__name__} ---")
        self.profiler.enable()
        result = func(*args, **kwargs)
        self.profiler.disable()
        
        # Create pstats.Stats object from the profiler
        s = io.StringIO()
        self.stats = pstats.Stats(self.profiler, stream=s)
        print("Profiling complete.")
        return result

    def get_report(self, sort_by: str = 'cumulative', top_n: int = 20) -> str:
        """
        Generates a formatted string report from the profiling statistics.

        Args:
            sort_by (str): The metric to sort the results by. Common values are:
                         'calls' (call count),
                         'cumulative' (cumulative time),
                         'tottime' (total time in function),
                         'pcalls' (primitive call count).
            top_n (int): The number of top functions to include in the report.

        Returns:
            str: A formatted profiling report.
        
        Raises:
            ValueError: If an invalid sort key is provided.
            RuntimeError: If profiling has not been run yet.
        """
        if not self.stats:
            raise RuntimeError("Profiling has not been run. Call profile_function first.")

        valid_sort_keys = ['calls', 'cumulative', 'tottime', 'pcalls', 'ncalls', 'cumtime', 'time']
        if sort_by not in valid_sort_keys:
            raise ValueError(f"Invalid sort key '{sort_by}'. Valid keys are: {valid_sort_keys}")

        s = io.StringIO()
        self.stats.strip_dirs().sort_stats(sort_by).print_stats(top_n)
        return s.getvalue()

    def save_report(self, file_path: str, sort_by: str = 'cumulative', top_n: int = 50):
        """
        Saves the detailed profiling report to a file.

        Args:
            file_path (str): The path to save the report file.
            sort_by (str): The metric to sort the results by.
            top_n (int): The number of top functions to include.
        """
        if not self.stats:
            raise RuntimeError("Profiling has not been run. Call profile_function first.")
        
        report = self.get_report(sort_by=sort_by, top_n=top_n)
        try:
            with open(file_path, 'w') as f:
                f.write(report)
            print(f"CPU profiling report saved to {file_path}")
        except IOError as e:
            print(f"Error saving report to {file_path}: {e}")

if __name__ == '__main__':
    # Example usage: Profile a sample function to demonstrate the profiler.

    def example_function_to_profile(limit=1000000):
        """A sample function with some computation to profile."""
        total = 0
        for i in range(limit):
            total += i
        return total

    def another_slow_function(limit=500000):
        """Another function that calls the first one."""
        return sum(i*i for i in range(limit))
    
    def main_task():
        example_function_to_profile()
        another_slow_function()

    print("--- Running CPU Profiler on Sample Functions ---")
    profiler = CPUProfiler()
    profiler.profile_function(main_task)
    
    print("\n--- Top 20 cumulative time ---")
    report = profiler.get_report(sort_by='cumulative', top_n=20)
    print(report)

    # Save a more detailed report to a file
    profiler.save_report("cpu_profile_report.txt", sort_by='tottime', top_n=50)

