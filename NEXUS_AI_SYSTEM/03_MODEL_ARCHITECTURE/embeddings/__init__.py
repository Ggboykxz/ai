
# --- NEXUS_AI_SYSTEM/03_MODEL_ARCHITECTURE/embeddings/__init__.py ---

import torch
import torch.nn as nn

# Référence à la configuration centrale du modèle.
# Le chemin d'importation est relatif à la racine du système NEXUS_AI.
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.core.model_config import ModelConfig

class NexusEmbeddings(nn.Module):
    """
    Couche d'embedding pour le modèle Nexus.

    Cette classe gère la conversion des tokens d'entrée en vecteurs denses.
    Elle inclut uniquement les embeddings de tokens. L'embedding positionnel
    sera géré via les Rotary Positional Embeddings (RoPE) directement dans
    les couches d'attention pour une meilleure performance et une gestion
    dynamique de la longueur de séquence.
    """
    def __init__(self, config: ModelConfig):
        """
        Initialise la couche d'embedding.

        Args:
            config (ModelConfig): L'objet de configuration contenant les
                                  hyperparamètres du modèle.
        """
        super().__init__()
        
        self.word_embeddings = nn.Embedding(
            config.vocab_size,
            config.hidden_size
        )
        
        self.config = config

    def forward(self, input_ids: torch.LongTensor) -> torch.Tensor:
        """
        Passe les IDs de tokens à travers la couche d'embedding.

        Args:
            input_ids (torch.LongTensor): Un tenseur de forme
                                          (batch_size, sequence_length)
                                          contenant les IDs des tokens.

        Returns:
            torch.Tensor: Les embeddings correspondants, de forme
                          (batch_size, sequence_length, hidden_size).
        """
        
        # 1. Obtenir les embeddings de mots.
        embeddings = self.word_embeddings(input_ids)
        
        # 2. Mise à l'échelle des embeddings (pratique courante).
        # Dans les architectures modernes, cela peut être combiné avec d'autres
        # normalisations, mais c'est une base solide.
        embeddings = embeddings * (self.config.hidden_size ** 0.5)

        return embeddings

