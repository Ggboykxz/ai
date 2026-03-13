
# --- NEXUS_AI_SYSTEM/03_MODEL_ARCHITECTURE/transformer/__init__.py ---

import torch
import torch.nn as nn
from typing import Optional

# Référence à la configuration centrale et aux sous-composants
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.core.model_config import ModelConfig
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.attention_mechanisms import NexusAttention
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.feed_forward import NexusFeedForward

class NexusRMSNorm(nn.Module):
    """
    Implémentation de la Root Mean Square Layer Normalization (RMSNorm).

    RMSNorm est une simplification de la LayerNorm traditionnelle qui est plus
    efficace en termes de calcul. Elle normalise les activations en utilisant
    la moyenne quadratique et les met à l'échelle avec un gain appris.
    """
    def __init__(self, hidden_size: int, eps: float = 1e-6):
        """
        Initialise la couche RMSNorm.

        Args:
            hidden_size (int): La dimension de la couche cachée.
            eps (float): Une petite valeur ajoutée pour la stabilité numérique.
        """
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.variance_epsilon = eps

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        """
        Applique la normalisation RMS aux états cachés.
        """
        # Convertit en float32 pour la stabilité du calcul de la variance
        input_dtype = hidden_states.dtype
        hidden_states = hidden_states.to(torch.float32)

        # Calcul de la variance et de l'inverse de la racine carrée (rsqrt)
        variance = hidden_states.pow(2).mean(-1, keepdim=True)
        hidden_states = hidden_states * torch.rsqrt(variance + self.variance_epsilon)

        # Remet à l'échelle avec le poids appris et reconvertit au dtype original
        return (self.weight * hidden_states).to(input_dtype)


class NexusTransformerBlock(nn.Module):
    """
    Un bloc décodeur unique du modèle Transformer Nexus.

    Ce bloc orchestre le flux de données à travers la normalisation, l'attention,
    les connexions résiduelles et la couche feed-forward.
    """
    def __init__(self, config: ModelConfig):
        super().__init__()
        self.hidden_size = config.hidden_size
        
        self.input_layernorm = NexusRMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.self_attn = NexusAttention(config)
        
        self.post_attention_layernorm = NexusRMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.mlp = NexusFeedForward(config)

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None
    ) -> torch.Tensor:
        """
        Passe avant à travers le bloc Transformer.

        Args:
            hidden_states (torch.Tensor): Entrée du bloc.
            attention_mask (Optional[torch.Tensor]): Masque pour éviter l'attention sur le padding.
            position_ids (Optional[torch.LongTensor]): IDs de position pour RoPE.

        Returns:
            torch.Tensor: La sortie du bloc Transformer.
        """
        # --- Première sous-couche: Attention Multi-Têtes ---
        
        # 1. Connexion résiduelle (entrée de la sous-couche)
        residual = hidden_states
        
        # 2. Normalisation pré-attention
        hidden_states = self.input_layernorm(hidden_states)
        
        # 3. Couche d'attention
        hidden_states = self.self_attn(
            hidden_states=hidden_states,
            attention_mask=attention_mask,
            position_ids=position_ids,
        )
        
        # 4. Ajout de la connexion résiduelle
        hidden_states = residual + hidden_states

        # --- Deuxième sous-couche: Feed-Forward Network ---

        # 1. Connexion résiduelle
        residual = hidden_states
        
        # 2. Normalisation pré-FFN
        hidden_states = self.post_attention_layernorm(hidden_states)
        
        # 3. Couche Feed-Forward (MLP)
        hidden_states = self.mlp(hidden_states)
        
        # 4. Ajout de la connexion résiduelle
        hidden_states = residual + hidden_states
        
        return hidden_states
