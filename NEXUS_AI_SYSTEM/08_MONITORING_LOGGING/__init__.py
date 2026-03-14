
# --- NEXUS_AI_SYSTEM/08_MONITORING_LOGGING/__init__.py ---

import json
import os
from datetime import datetime

class NexusLogger:
    """
    Gère la journalisation structurée des exécutions d'entraînement et d'évaluation.
    Les logs sont sauvegardés au format JSON Lines (.jsonl).
    """
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.log_file = os.path.join(self.log_dir, "run_history.jsonl")

    def log_run(self, run_type: str, metrics: dict, config: dict, checkpoint_path: str = None):
        """
        Enregistre une seule exécution (run) dans le fichier de log.

        Args:
            run_type (str): Le type d'exécution ('training' ou 'evaluation').
            metrics (dict): Un dictionnaire contenant les métriques clés (ex: {'loss': 0.1, 'accuracy': 0.9}).
            config (dict): La configuration utilisée pour cette exécution.
            checkpoint_path (str, optional): Le chemin vers le checkpoint du modèle utilisé ou sauvegardé.
        """
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'run_type': run_type,
            'metrics': metrics,
            'config': config,
            'checkpoint_path': checkpoint_path
        }

        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
            print(f"Résultats de l'exécution de type '{run_type}' enregistrés dans {self.log_file}")
        except IOError as e:
            print(f"ERREUR: Impossible d'écrire dans le fichier de log {self.log_file}. Erreur: {e}")

