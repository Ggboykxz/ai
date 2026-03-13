
# --- NEXUS_AI_SYSTEM/03_MODEL_ARCHITECTURE/attention_mechanisms/__init__.py ---

import torch
import torch.nn as nn
from typing import Tuple

# Référence à la configuration centrale du modèle.
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.core.model_config import ModelConfig

class NexusRotaryEmbedding(nn.Module):
    """
    Implémentation des Rotary Positional Embeddings (RoPE).

    RoPE encode l'information de position absolue en appliquant une rotation
    aux vecteurs de Query et Key, ce qui permet au modèle de déduire
    l'information de position relative via le produit scalaire de l'attention.
    
    Cette classe pré-calcule les fréquences de rotation pour une efficacité maximale.
    """
    def __init__(self, dim: int, max_position_embeddings: int = 2048, base: int = 10000):
        """
        Initialise les RoPE.

        Args:
            dim (int): La dimension des vecteurs à faire pivoter (généralement head_dim).
            max_position_embeddings (int): La longueur de séquence maximale supportée.
            base (int): La base utilisée pour calculer les fréquences de rotation.
        """
        super().__init__()
        self.dim = dim
        self.max_position_embeddings = max_position_embeddings
        self.base = base

        # Pré-calcul des fréquences (theta).
        # inv_freq shape: (dim / 2)
        inv_freq = 1.0 / (self.base ** (torch.arange(0, self.dim, 2).float() / self.dim))
        self.register_buffer("inv_freq", inv_freq)

        # Pré-calcul et mise en cache des embeddings cos/sin.
        self._set_cos_sin_cache(seq_len=max_position_embeddings)

    def _set_cos_sin_cache(self, seq_len: int):
        """
        Calcule et met en cache les valeurs de cosinus et sinus pour une longueur de séquence donnée.
        """
        self.max_seq_len_cached = seq_len
        t = torch.arange(self.max_seq_len_cached, device=self.inv_freq.device, dtype=self.inv_freq.dtype)

        # Calcule les fréquences pour chaque position.
        # freqs shape: (seq_len, dim / 2)
        freqs = torch.einsum("i,j->ij", t, self.inv_freq)
        
        # Concatène pour obtenir la forme (seq_len, dim) pour une manipulation plus facile.
        emb = torch.cat((freqs, freqs), dim=-1)
        
        # Cache cos et sin. Shape: (1, 1, seq_len, dim)
        self.register_buffer("cos_cached", emb.cos()[None, None, :, :], persistent=False)
        self.register_buffer("sin_cached", emb.sin()[None, None, :, :], persistent=False)

    def forward(self, x: torch.Tensor, seq_len: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Retourne les embeddings cos/sin pour la séquence donnée.
        """
        # Si la séquence est plus longue que le cache, le recalculer.
        if seq_len > self.max_seq_len_cached:
            self._set_cos_sin_cache(seq_len)

        return (
            self.cos_cached[:, :, :seq_len, ...],
            self.sin_cached[:, :, :seq_len, ...],
        )


def rotate_half(x: torch.Tensor) -> torch.Tensor:
    """Fait pivoter la moitié des features de la dernière dimension."""
    # Sépare la dernière dimension en deux moitiés
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2 :]
    # Concatène avec la polarité inversée et l'ordre changé
    return torch.cat((-x2, x1), dim=-1)


def apply_rotary_pos_emb(
    q: torch.Tensor, k: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Applique les Rotary Positional Embeddings aux vecteurs Query et Key.

    Args:
        q (torch.Tensor): Tenseur des Queries (batch, num_heads, seq_len, head_dim).
        k (torch.Tensor): Tenseur des Keys (batch, num_heads, seq_len, head_dim).
        cos (torch.Tensor): Tenseur des cosinus pré-calculés.
        sin (torch.Tensor): Tenseur des sinus pré-calculés.

    Returns:
        Tuple[torch.Tensor, torch.Tensor]: Les tenseurs Q et K avec les positions encodées.
    """
    # Applique la rotation.
    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    return q_embed, k_embed

