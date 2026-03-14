
# --- NEXUS_AI_SYSTEM/main.py ---

import torch
import yaml
from pathlib import Path
from transformers import GPT2Tokenizer

# Import des composants du système Nexus AI
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.core.model_config import ModelConfig
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.model import NexusForCausalLM
from NEXUS_AI_SYSTEM.04_DATA_PIPELINE import CausalLMDataset
from NEXUS_AI_SYSTEM.05_TRAINING import NexusTrainer
from NEXUS_AI_SYSTEM.08_MONITORING_LOGGING import NexusLogger # <-- NOUVEAU

def load_config(config_path: str) -> dict:
    """Charge la configuration depuis un fichier YAML."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def run_training_pipeline():
    """Exécute le pipeline d'entraînement complet, du chargement des données à la sauvegarde du modèle."""
    print("--- Lancement du pipeline d'entraînement de NEXUS-AI ---")

    # --- 1. Configuration ---
    config_path = Path(__file__).parent / "config/default.yaml"
    config = load_config(config_path)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # --- 2. Préparation des Données ---
    tokenizer = GPT2Tokenizer.from_pretrained(config['data']['tokenizer_name'])
    corpus_path = Path(__file__).parent / config['data']['corpus_path']
    with open(corpus_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    tokenized_data = tokenizer.encode(text)
    # Assurer que vocab_size correspond bien au tokenizer
    config['model']['vocab_size'] = tokenizer.vocab_size

    train_dataset = CausalLMDataset(
        tokenized_data=tokenized_data, 
        block_size=config['model']['block_size']
    )
    print(f"Jeu de données d\'entraînement chargé avec {len(train_dataset)} exemples.")

    # --- 3. Initialisation du Modèle ---
    model_config = ModelConfig(**config['model'])
    model = NexusForCausalLM(model_config)
    print(f"Modèle initialisé avec {model.count_parameters():,} paramètres.")

    # --- 4. Entraînement ---
    trainer = NexusTrainer(
        model=model,
        train_dataset=train_dataset,
        learning_rate=config['training']['learning_rate'],
        batch_size=config['training']['batch_size'],
        epochs=config['training']['epochs'],
        device=device
    )
    final_loss, checkpoint_path = trainer.train()

    # --- 5. Journalisation (Logging) ---
    logger = NexusLogger()
    logger.log_run(
        run_type='training',
        metrics={'final_average_loss': final_loss},
        config=config,
        checkpoint_path=checkpoint_path
    )

    print("\n--- Pipeline d'entraînement terminé avec succès ---")

if __name__ == "__main__":
    run_training_pipeline()
