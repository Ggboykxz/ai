
# --- NEXUS_AI_SYSTEM/generate.py ---

import torch
import yaml
from pathlib import Path
from transformers import GPT2Tokenizer

# Import des composants du système Nexus AI
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.core.model_config import ModelConfig
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.model import NexusForCausalLM

def load_config(config_path: str) -> dict:
    """Charge la configuration depuis un fichier YAML."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def run_generation(
    prompt: str = "L'intelligence artificielle est", 
    max_new_tokens: int = 50, 
    temperature: float = 0.8,
    checkpoint_path: str = "checkpoints/nexus_model_final.pth"
):
    """
    Charge un modèle Nexus entraîné et génère du texte à partir d'un prompt.
    """
    print("--- Lancement de la génération de texte avec NEXUS-AI ---")

    # --- 1. Configuration ---
    config_path = Path(__file__).parent / "config/default.yaml"
    config = load_config(config_path)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Utilisation du périphérique : {device}")

    # --- 2. Initialisation du Tokenizer ---
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    config['model']['vocab_size'] = tokenizer.vocab_size

    # --- 3. Initialisation du Modèle ---
    model_config = ModelConfig(**config['model'])
    model = NexusForCausalLM(model_config).to(device)

    # --- 4. Chargement des Poids ---
    try:
        model.load_state_dict(torch.load(checkpoint_path, map_location=device))
        print(f"Poids du modèle chargés depuis {checkpoint_path}")
    except FileNotFoundError:
        print(f"ERREUR: Le fichier de checkpoint '{checkpoint_path}' n'a pas été trouvé.")
        print("Veuillez d'abord entraîner un modèle en exécutant 'python NEXUS_AI_SYSTEM/main.py'")
        return

    model.eval()

    # --- 5. Génération ---
    print(f"\nPrompt : '{prompt}'")
    print("Génération en cours...")

    # Tokeniser le prompt
    input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)

    # Générer la séquence
    output_ids = model.generate(
        input_ids=input_ids, 
        max_new_tokens=max_new_tokens, 
        temperature=temperature
    )

    # Décoder la sortie
    generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    print("\n--- Résultat ---")
    print(generated_text)
    print("\n-----------------")

if __name__ == "__main__":
    # Vous pouvez modifier le prompt et les paramètres ici
    run_generation(prompt="Le futur de l'IA est", max_new_tokens=100)

