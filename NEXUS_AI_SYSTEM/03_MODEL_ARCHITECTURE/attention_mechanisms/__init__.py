
# --- NEXUS_AI_SYSTEM/03_MODEL_ARCHITECTURE/attention_mechanisms/__init__.py ---

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional

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
    def __init__(self, dim: int, max_position_embeddings: int = 4096, base: int = 10000):
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

        inv_freq = 1.0 / (self.base ** (torch.arange(0, self.dim, 2).float() / self.dim))
        self.register_buffer("inv_freq", inv_freq)

        self._set_cos_sin_cache(seq_len=max_position_embeddings)

    def _set_cos_sin_cache(self, seq_len: int):
        self.max_seq_len_cached = seq_len
        t = torch.arange(self.max_seq_len_cached, device=self.inv_freq.device, dtype=self.inv_freq.dtype)
        freqs = torch.einsum("i,j->ij", t, self.inv_freq)
        emb = torch.cat((freqs, freqs), dim=-1)
        self.register_buffer("cos_cached", emb.cos()[None, None, :, :], persistent=False)
        self.register_buffer("sin_cached", emb.sin()[None, None, :, :], persistent=False)

    def forward(self, x: torch.Tensor, seq_len: int) -> Tuple[torch.Tensor, torch.Tensor]:
        if seq_len > self.max_seq_len_cached:
            self._set_cos_sin_cache(seq_len)
        return self.cos_cached[:, :, :seq_len, ...], self.sin_cached[:, :, :seq_len, ...]

def rotate_half(x: torch.Tensor) -> torch.Tensor:
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2 :]
    return torch.cat((-x2, x1), dim=-1)

def apply_rotary_pos_emb(
    q: torch.Tensor, k: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor
) -> Tuple[torch.Tensor, torch.Tensor]:
    q_embed = (q * cos) + (rotate_half(q) * sin)
    k_embed = (k * cos) + (rotate_half(k) * sin)
    return q_embed, k_embed


class NexusAttention(nn.Module):
    """
    Couche d'attention multi-têtes (Multi-Head Attention) pour le modèle Nexus.

    Cette implémentation intègre :
    - Projections linéaires pour Q, K, V.
    - Rotary Positional Embeddings (RoPE) pour l'encodage de position.
    - Scaled Dot-Product Attention (avec support potentiel pour Flash Attention).
    - Projection de sortie.
    """
    def __init__(self, config: ModelConfig):
        super().__init__()
        self.config = config
        self.hidden_size = config.hidden_size
        self.num_heads = config.num_attention_heads
        self.head_dim = self.hidden_size // self.num_heads

        self.q_proj = nn.Linear(self.hidden_size, self.hidden_size, bias=False)
        self.k_proj = nn.Linear(self.hidden_size, self.hidden_size, bias=False)
        self.v_proj = nn.Linear(self.hidden_size, self.hidden_size, bias=False)
        self.o_proj = nn.Linear(self.hidden_size, self.hidden_size, bias=False)
        
        self.rotary_emb = NexusRotaryEmbedding(self.head_dim)

    def forward(
        self, 
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None
    ) -> torch.Tensor:
        
        bsz, q_len, _ = hidden_states.size()

        query_states = self.q_proj(hidden_states).view(bsz, q_len, self.num_heads, self.head_dim).transpose(1, 2)
        key_states = self.k_proj(hidden_states).view(bsz, q_len, self.num_heads, self.head_dim).transpose(1, 2)
        value_states = self.v_proj(hidden_states).view(bsz, q_len, self.num_heads, self.head_dim).transpose(1, 2)

        cos, sin = self.rotary_emb(value_states, seq_len=q_len)
        query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin)
        
        # Utilisation de l'implémentation optimisée de PyTorch
        attn_output = F.scaled_dot_product_attention(
            query_states, 
            key_states, 
            value_states, 
            attn_mask=attention_mask
        )

        attn_output = attn_output.transpose(1, 2).contiguous().view(bsz, q_len, self.hidden_size)
        attn_output = self.o_proj(attn_output)
        
        return attn_output
