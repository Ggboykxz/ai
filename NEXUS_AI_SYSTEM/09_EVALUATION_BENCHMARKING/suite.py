# --- NEXUS_AI_SYSTEM/09_EVALUATION_BENCHMARKING/evaluation_suite.py ---

from typing import Dict, Any, List
import json

# Use relative imports to bring in the necessary components.
from .runners.benchmark_runner import BenchmarkRunner
from .metrics.metrics_calculator import MetricsCalculator

# As before, we need an inference engine to run evaluations.
from ..inference_engine import InferenceEngine

class EvaluationSuite:
    """
    Coordinates the entire evaluation process, from running benchmarks to reporting results.
    """

    def __init__(self, inference_engine: InferenceEngine, benchmarks: Dict[str, List[Dict]]):
        """
        Initializes the evaluation suite.

        Args:
            inference_engine (InferenceEngine): The engine to evaluate.
            benchmarks (Dict[str, List[Dict]]): A dictionary where keys are benchmark names
                                                and values are the dataset for that benchmark.
        """
        self.inference_engine = inference_engine
        self.benchmarks = benchmarks
        self.full_report = {}

    def run_and_evaluate(self) -> Dict[str, Any]:
        """
        Runs all registered benchmarks and calculates metrics for each.

        Returns:
            Dict[str, Any]: A comprehensive report of all benchmark results and metrics.
        """
        print(f"--- Starting Evaluation Suite for {len(self.benchmarks)} benchmarks... ---")
        
        for name, dataset in self.benchmarks.items():
            # 1. Run the benchmark
            runner = BenchmarkRunner(benchmark_name=name, 
                                     inference_engine=self.inference_engine, 
                                     dataset=dataset)
            benchmark_results = runner.run()

            # 2. Calculate metrics from the results
            calculator = MetricsCalculator(raw_results=benchmark_results["raw_results"])
            metrics = calculator.calculate()

            # 3. Store the results in a structured report
            self.full_report[name] = {
                "summary": {
                    "item_count": benchmark_results["item_count"],
                    "total_time_seconds": benchmark_results["total_time_seconds"],
                    "metrics": metrics
                },
                "raw_results": benchmark_results["raw_results"]
            }

        print("--- Evaluation Suite finished. ---")
        return self.full_report

# Example Usage
if __name__ == '__main__':
    print("--- Running Evaluation Suite Example ---")

    # 1. Set up the necessary components
    try:
        # Use the real (simulated) engine if possible
        from ...inference_engine import InferenceEngine as RealInferenceEngine
        engine = RealInferenceEngine(model_path="nexus-ai/eval-suite-model-simulated")
    except (ImportError, ModuleNotFoundError):
        print("Using a mock engine for this example.")
        class MockInferenceEngine:
            def run(self, prompt: str, params=None) -> str:
                if "capital of France" in prompt: return "Paris"
                if "meaning of life" in prompt: return "A philosophical question."
                return "Simulated generic response."
        engine = MockInferenceEngine()

    # 2. Define the benchmarks to run
    # In a real system, these would be loaded from files (e.g., JSONL).
    benchmarks_to_run = {
        "Simple-QA": [
            {"prompt": "What is the capital of France?", "reference_answer": "Paris"},
            {"prompt": "What is the meaning of life?", "reference_answer": "42"}
        ],
        "Coding-Eval": [
            {"prompt": "def f(x): return x+1", "reference_answer": "def f(x): return x+1"}
        ]
    }

    # 3. Initialize and run the suite
    suite = EvaluationSuite(inference_engine=engine, benchmarks=benchmarks_to_run)
    final_report = suite.run_and_evaluate()

    # 4. Print the final report
    print("\n--- Final Evaluation Report ---")
    print(json.dumps(final_report, indent=2))

