# --- NEXUS_AI_SYSTEM/10_RESEARCH_LAB/experiments/experiment_runner.py ---

from typing import Dict, Any
import time
import uuid

class ExperimentRunner:
    """
    Manages a single, isolated machine learning experiment.

    This class simulates the process of running a training job with a specific
    model configuration and dataset, and then evaluating the resulting model.
    """

    def __init__(self, experiment_config: Dict[str, Any]):
        """
        Initializes the experiment with a given configuration.

        Args:
            experiment_config (Dict[str, Any]): A dictionary defining the experiment,
                including model architecture, training parameters, and dataset details.
        """
        self.experiment_id = f"exp_{uuid.uuid4().hex[:8]}"
        self.config = experiment_config
        self.model_name = self.config.get("model_name", "default_model")
        self.dataset = self.config.get("dataset", "default_dataset")
        self.hyperparameters = self.config.get("hyperparameters", {})
        
    def run(self) -> Dict[str, Any]:
        """
        Simulates the entire experiment lifecycle.

        Returns:
            Dict[str, Any]: A report summarizing the experiment and its outcome.
        """
        print(f"--- Starting Experiment: {self.experiment_id} ({self.model_name}) ---")
        print(f"Dataset: {self.dataset}")
        print(f"Hyperparameters: {self.hyperparameters}")

        # 1. Simulate the training process
        training_duration = self._simulate_training()
        
        # 2. Simulate the evaluation process
        evaluation_results = self._simulate_evaluation()

        # 3. Compile the final report
        report = {
            "experiment_id": self.experiment_id,
            "config": self.config,
            "status": "completed",
            "results": {
                "training_duration_seconds": training_duration,
                "evaluation_metrics": evaluation_results
            }
        }

        print(f"--- Experiment {self.experiment_id} finished. ---")
        return report

    def _simulate_training(self) -> float:
        """
        A private method to simulate a model training job.
        The duration can be influenced by hyperparameters.
        """
        epochs = self.hyperparameters.get("epochs", 3)
        learning_rate = self.hyperparameters.get("learning_rate", 0.01)
        
        print(f"Simulating training for {epochs} epochs with lr={learning_rate}...")
        # Simulate a longer training time for more epochs
        training_time = 2.0 * epochs 
        time.sleep(training_time)
        print("Training simulation complete.")
        return training_time

    def _simulate_evaluation(self) -> Dict[str, float]:
        """
        A private method to simulate model evaluation and generate fake metrics.
        """
        print("Simulating evaluation...")
        time.sleep(0.5)
        
        # Generate metrics based on config to make it interesting
        accuracy = 0.85 + (len(self.model_name) % 5) / 100.0 # Trivial heuristic
        loss = 0.15 - (self.hyperparameters.get("learning_rate", 0.01) * 2)

        print("Evaluation simulation complete.")
        return {
            "accuracy": round(accuracy, 4),
            "loss": round(loss, 4),
            "exact_match": round(accuracy - 0.1, 4) # Another fake metric
        }

if __name__ == '__main__':
    print("--- Running Experiment Runner Example ---")

    # 1. Define an experiment configuration
    exp_config = {
        "model_name": "TinyTransformer-v1",
        "dataset": "wikitext-103-simulated",
        "hyperparameters": {
            "epochs": 5,
            "learning_rate": 0.001,
            "batch_size": 32
        }
    }

    # 2. Initialize and run the experiment
    runner = ExperimentRunner(experiment_config=exp_config)
    experiment_report = runner.run()

    # 3. Print the results
    print("\n--- Experiment Report ---")
    import json
    print(json.dumps(experiment_report, indent=2))

    # --- Second Example ---
    print("\n--- Running a second, different experiment ---")
    exp_config_2 = {
        "model_name": "SimpleRNN-v2",
        "dataset": "imdb-reviews-simulated",
        "hyperparameters": {
            "epochs": 2,
            "learning_rate": 0.05
        }
    }
    runner_2 = ExperimentRunner(experiment_config=exp_config_2)
    experiment_report_2 = runner_2.run()
    print("\n--- Experiment Report 2 ---")
    print(json.dumps(experiment_report_2, indent=2))

