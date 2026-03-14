# --- NEXUS_AI_SYSTEM/10_RESEARCH_LAB/lab_manager.py ---

from typing import Dict, Any, List
import json

# Use a relative import to bring in the experiment runner
from .experiments.experiment_runner import ExperimentRunner

class LabManager:
    """
    Manages and orchestrates multiple research experiments.

    This class can run a series of experiments, collect their reports,
    and provide a summary of all conducted research.
    """

    def __init__(self, experiment_configs: List[Dict[str, Any]]):
        """
        Initializes the Lab Manager with a list of experiment configurations.

        Args:
            experiment_configs (List[Dict[str, Any]]): A list of configurations,
                where each configuration defines an experiment to be run.
        """
        self.experiment_configs = experiment_configs
        self.all_reports = []

    def run_all_experiments(self):
        """
        Executes all experiments defined in the initial configurations.
        """
        print(f"--- Lab Manager starting: {len(self.experiment_configs)} experiments to run. ---")
        
        for i, config in enumerate(self.experiment_configs):
            print(f"\n--- Preparing Experiment {i + 1}/{len(self.experiment_configs)} ---")
            
            # Initialize and run a single experiment
            runner = ExperimentRunner(experiment_config=config)
            report = runner.run()
            self.all_reports.append(report)

        print(f"\n--- Lab Manager finished: All {len(self.experiment_configs)} experiments complete. ---")

    def get_summary_report(self) -> str:
        """
        Generates a JSON summary of all experiment reports.

        Returns:
            str: A JSON formatted string containing all the reports.
        """
        return json.dumps(self.all_reports, indent=2)

if __name__ == '__main__':
    print("--- Running Lab Manager Example ---")

    # 1. Define a list of experiment configurations to run
    # This could come from a YAML file or a database in a real system.
    configs = [
        {
            "model_name": "LLM-v1-A",
            "dataset": "internal-corpus-v1",
            "hyperparameters": {"epochs": 3, "learning_rate": 0.01}
        },
        {
            "model_name": "LLM-v1-B-tuned",
            "dataset": "internal-corpus-v1",
            "hyperparameters": {"epochs": 3, "learning_rate": 0.005, "dropout": 0.1}
        },
        {
            "model_name": "LLM-v1-A",
            "dataset": "public-corpus-v2",
            "hyperparameters": {"epochs": 5, "learning_rate": 0.01}
        }
    ]

    # 2. Initialize the manager with the configurations
    lab_manager = LabManager(experiment_configs=configs)

    # 3. Run all the experiments
    lab_manager.run_all_experiments()

    # 4. Get and print the final summary report
    summary = lab_manager.get_summary_report()
    print("\n--- Lab Manager Final Summary Report ---")
    print(summary)

