
# --- NEXUS_AI_SYSTEM/03_MODEL_ARCHITECTURE/feed_forward/__init__.py ---

import torch
import torch.nn as nn
import torch.nn.functional as F

# Référence à la configuration centrale du modèle.
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.core.model_config import ModelConfig

class NexusFeedForward(nn.Module):
    """
    Couche Feed-Forward (FFN) utilisant une non-linéarité SwiGLU.

    Cette architecture est plus performante que les MLP traditionnels basés sur ReLU.
    Elle se compose de trois projections linéaires : "gate", "up", et "down".
    La sortie est calculée comme : Down(Swish(Gate(x)) * Up(x))
    """
    def __init__(self, config: ModelConfig):
        super().__init__()

        self.gate_proj = nn.Linear(config.hidden_size, config.intermediate_size, bias=False)
        self.up_proj = nn.Linear(config.hidden_size, config.intermediate_size, bias=False)
        self.down_proj = nn.Linear(config.intermediate_size, config.hidden_size, bias=False)
        self.act_fn = F.silu  # Swish activation function (SiLU)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Passe le tenseur d'entrée à travers la couche FFN.

        Args:
            x (torch.Tensor): Le tenseur de sortie de la couche d'attention,
                              de forme (batch_size, seq_len, hidden_size).

        Returns:
            torch.Tensor: Le tenseur de sortie, de même forme.
        """
        
        # 1. Projections "gate" et "up".
        gate = self.act_fn(self.gate_proj(x))
        up = self.up_proj(x)
        
        # 2. Multiplication élément par élément (mécanisme de gating).
        fused_gate_up = gate * up
        
        # 3. Projection "down" pour ramener à la dimension cachée.
        output = self.down_proj(fused_gate_up)
        
        return output
