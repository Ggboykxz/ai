
# --- NEXUS_AI_SYSTEM/evaluate.py ---

import torch
import yaml
from pathlib import Path
from transformers import GPT2Tokenizer

# Import des composants du système Nexus AI
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.core.model_config import ModelConfig
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.model import NexusForCausalLM
from NEXUS_AI_SYSTEM.04_DATA_PIPELINE import CausalLMDataset
from NEXUS_AI_SYSTEM.07_EVALUATION import calculate_perplexity
from NEXUS_AI_SYSTEM.08_MONITORING_LOGGING import NexusLogger # <-- NOUVEAU

def load_config(config_path: str) -> dict:
    """Charge la configuration depuis un fichier YAML."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def run_evaluation(checkpoint_path: str = "checkpoints/nexus_model_final.pth"):
    """
    Charge un modèle Nexus entraîné et évalue sa perplexité sur un jeu de données de validation.
    """
    print("--- Lancement de l'évaluation du modèle NEXUS-AI ---")

    # --- 1. Configuration ---
    config_path = Path(__file__).parent / "config/default.yaml"
    config = load_config(config_path)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # --- 2. Initialisation du Tokenizer ---
    tokenizer = GPT2Tokenizer.from_pretrained(config['data']['tokenizer_name'])
    config['model']['vocab_size'] = tokenizer.vocab_size

    # --- 3. Préparation des Données de Validation ---
    validation_corpus_path = Path(__file__).parent / "data/validation.txt"
    with open(validation_corpus_path, 'r', encoding='utf-8') as f:
        validation_text = f.read()

    tokenized_validation_data = tokenizer.encode(validation_text)
    validation_dataset = CausalLMDataset(
        tokenized_data=tokenized_validation_data, 
        block_size=config['model']['block_size']
    )

    # --- 4. Initialisation du Modèle ---
    model_config = ModelConfig(**config['model'])
    model = NexusForCausalLM(model_config)

    # --- 5. Chargement des Poids ---
    try:
        model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    except FileNotFoundError:
        print(f"ERREUR: Le fichier de checkpoint '{checkpoint_path}' n'a pas été trouvé.")
        return

    # --- 6. Évaluation ---
    perplexity = calculate_perplexity(
        model=model,
        dataset=validation_dataset,
        batch_size=config['training']['batch_size'],
        device=device
    )

    # --- 7. Journalisation (Logging) ---
    logger = NexusLogger()
    logger.log_run(
        run_type='evaluation',
        metrics={'perplexity': perplexity},
        config=config,
        checkpoint_path=checkpoint_path
    )

    print(f"\nPerplexité finale : {perplexity:.4f}")
    print("--- Évaluation terminée ---")

if __name__ == "__main__":
    run_evaluation()

