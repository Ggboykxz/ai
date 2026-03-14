# --- NEXUS_AI_SYSTEM/05_SELF_IMPROVEMENT_ENGINE/code_analysis/gpu_profiler.py ---

import torch
from torch.profiler import profile, record_function, ProfilerActivity
from typing import Callable, Any, List

class GPUProfiler:
    """
    A wrapper for PyTorch's built-in profiler to analyze GPU and CPU performance
    of PyTorch models and operations.

    This profiler is essential for identifying bottlenecks in:
    - GPU kernel execution times.
    - CPU overhead in deep learning workloads.
    - Memory allocation on the GPU.
    - Data transfer times between CPU and GPU.
    """

    def __init__(self, activities: List[ProfilerActivity] = None, use_cuda: bool = True):
        """
        Initializes the GPU profiler.

        Args:
            activities (List[ProfilerActivity], optional): A list of activities to profile.
                Defaults to [ProfilerActivity.CPU, ProfilerActivity.CUDA].
            use_cuda (bool): Whether to profile CUDA events. Defaults to True.
        """
        if use_cuda and not torch.cuda.is_available():
            raise RuntimeError("CUDA is not available, but use_cuda was set to True.")
        
        self.use_cuda = use_cuda
        if activities is None:
            self.activities = [ProfilerActivity.CPU]
            if self.use_cuda:
                self.activities.append(ProfilerActivity.CUDA)
        else:
            self.activities = activities
        
        self.profiler: torch.profiler.profile = None

    def profile_function(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """
        Profiles a function using the torch.profiler context manager.

        Args:
            func (Callable): The function to profile.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.

        Returns:
            Any: The return value of the profiled function.
        """
        print(f"\n--- Profiling function with torch.profiler: {func.__name__} ---")
        with profile(activities=self.activities,
                       record_shapes=True,
                       profile_memory=True,
                       with_stack=True) as prof:
            with record_function(f"model_execution_{func.__name__}"):
                result = func(*args, **kwargs)
        
        self.profiler = prof
        print("GPU/CPU profiling complete.")
        return result

    def get_report(self, sort_by: str = "cuda_time_total", top_n: int = 20) -> str:
        """
        Generates a formatted report from the profiler data.

        Args:
            sort_by (str): The metric to sort the table by. 
                         E.g., 'cpu_time_total', 'cuda_time_total', 'self_cpu_memory_usage'.
            top_n (int): The number of top events to display.

        Returns:
            str: A string containing the profiler report.
        
        Raises:
            RuntimeError: If profiling has not been run yet.
        """
        if not self.profiler:
            raise RuntimeError("Profiling has not been run. Call profile_function first.")

        report = self.profiler.key_averages().table(sort_by=sort_by, row_limit=top_n)
        return report

    def save_chrome_trace(self, file_path: str):
        """
        Exports the profiling data as a Chrome trace file (.json).
        This trace can be loaded in Chrome's trace viewer (chrome://tracing).

        Args:
            file_path (str): The path to save the trace file.
        
        Raises:
            RuntimeError: If profiling has not been run yet.
        """
        if not self.profiler:
            raise RuntimeError("Profiling has not been run. Call profile_function first.")
        
        try:
            self.profiler.export_chrome_trace(file_path)
            print(f"Chrome trace saved to {file_path}")
        except Exception as e:
            print(f"Error saving Chrome trace: {e}")


if __name__ == '__main__':
    # Example usage: Profile a simple PyTorch model execution.

    def setup_and_run_model():
        """Sets up a simple model and runs a forward pass."""
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Running on device: {device}")

        # A simple model
        model = torch.nn.Sequential(
            torch.nn.Linear(128, 256),
            torch.nn.ReLU(),
            torch.nn.Linear(256, 512),
            torch.nn.ReLU(),
            torch.nn.Linear(512, 10)
        ).to(device)

        # Dummy input data
        inputs = torch.randn(64, 128).to(device)

        # Run the forward pass
        with torch.no_grad():
            model(inputs)

    print("--- Running GPU Profiler on a Sample PyTorch Model ---")
    use_gpu = torch.cuda.is_available()
    profiler = GPUProfiler(use_cuda=use_gpu)
    
    try:
        profiler.profile_function(setup_and_run_model)
        
        print("\n--- Profiler Report (sorted by CUDA total time) ---")
        report = profiler.get_report(sort_by="cuda_time_total" if use_gpu else "cpu_time_total", top_n=15)
        print(report)

        # Save a trace file for detailed analysis in Chrome Trace Viewer
        trace_file = "gpu_profile_trace.json"
        profiler.save_chrome_trace(trace_file)

    except RuntimeError as e:
        print(f"Profiler execution failed: {e}")
        print("This may happen if you don't have a CUDA-enabled GPU.")

