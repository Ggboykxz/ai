# --- NEXUS_AI_SYSTEM/09_EVALUATION_BENCHMARKING/metrics/metrics_calculator.py ---

from typing import Dict, Any, List, Callable

class MetricsCalculator:
    """
    Calculates performance metrics from the raw results of a benchmark run.
    
    This class is designed to be extensible with different metric functions.
    """

    def __init__(self, raw_results: List[Dict]):
        """
        Initializes the calculator with the raw benchmark results.

        Args:
            raw_results (List[Dict]): A list of dictionaries, where each dictionary
                                      contains 'model_answer' and 'reference_answer'.
        """
        if not raw_results:
            raise ValueError("Raw results cannot be empty.")
        self.raw_results = raw_results
        self.metrics = {}

    def calculate(self) -> Dict[str, Any]:
        """
        Runs all registered metric calculations and returns the results.

        Returns:
            Dict[str, Any]: A dictionary containing the calculated metrics.
        """
        print("--- Calculating metrics... ---")
        
        # For Generation 0, we will only calculate exact match.
        # In the future, this could be a dynamic list of metric functions.
        self._calculate_exact_match()
        # self._calculate_rouge_score() # Example of a future metric
        # self._calculate_bleu_score()  # Example of a future metric

        print(f"Metrics calculated: {self.metrics}")
        return self.metrics

    def _calculate_exact_match(self):
        """
        Calculates the exact match score.

        This metric measures the percentage of model answers that are identical
        to the reference answers.
        """
        if not self.raw_results:
            self.metrics['exact_match'] = {"score": 0, "total": 0, "correct": 0}
            return

        correct_count = 0
        total_count = len(self.raw_results)

        for result in self.raw_results:
            model_answer = str(result.get('model_answer', '')).strip()
            reference_answer = str(result.get('reference_answer', '')).strip()
            
            if model_answer == reference_answer:
                correct_count += 1

        score = (correct_count / total_count) if total_count > 0 else 0
        
        self.metrics['exact_match'] = {
            "score": round(score, 4),
            "total": total_count,
            "correct": correct_count
        }

# Example Usage
if __name__ == '__main__':
    print("--- Running Metrics Calculator Example ---")

    # 1. Sample raw results from a benchmark run
    sample_results = [
        {
            "model_answer": "Paris",
            "reference_answer": "Paris"
        },
        {
            "model_answer": "def hello():\n    print('Hello, World!')",
            "reference_answer": "def hello():\n    print('Hello, World!')"
        },
        {
            "model_answer": "A complex and philosophical question.",
            "reference_answer": "42" # This one will not match
        },
        {
            "model_answer": "  London  ", # It should be trimmed
            "reference_answer": "London"
        }
    ]

    # 2. Initialize the calculator and run calculations
    calculator = MetricsCalculator(raw_results=sample_results)
    calculated_metrics = calculator.calculate()

    # 3. Print the results
    print("\n--- Calculated Metrics ---")
    import json
    print(json.dumps(calculated_metrics, indent=2))

    # Example with no results
    print("\n--- Example with empty results ---")
    try:
        calculator_empty = MetricsCalculator(raw_results=[])
    except ValueError as e:
        print(f"Caught expected error: {e}")

