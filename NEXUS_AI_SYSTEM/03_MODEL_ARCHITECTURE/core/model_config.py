
from dataclasses import dataclass, field
from typing import Optional, Tuple

@dataclass
class ModelConfig:
    """
    Configuration de base pour les modèles de la famille Nexus.

    Cette classe contient tous les hyperparamètres nécessaires pour définir
    l'architecture d'un modèle, de la taille des embeddings à la configuration
    des couches spécifiques.
    """

    # --- Dimensions du modèle ---
    vocab_size: int = 65536
    hidden_size: int = 8192
    num_hidden_layers: int = 64
    num_attention_heads: int = 64
    
    # --- Configuration des couches ---
    intermediate_size: int = 32768
    activation_function: str = "silu"
    
    # --- Paramètres de régularisation ---
    dropout_prob: float = 0.1
    
    # --- Précision ---
    torch_dtype: str = "bfloat16"

    def __post_init__(self):
        """
        Valide les paramètres après l'initialisation.
        """
        if self.hidden_size % self.num_attention_heads != 0:
            raise ValueError(
                f"hidden_size ({self.hidden_size}) doit être divisible par "
                f"num_attention_heads ({self.num_attention_heads})"
            )

