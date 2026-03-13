
# --- NEXUS_AI_SYSTEM/03_MODEL_ARCHITECTURE/model.py ---

import torch
import torch.nn as nn
from typing import List, Optional, Tuple

# Références aux composants du modèle
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.core.model_config import ModelConfig
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.embeddings import NexusEmbedding
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.transformer import NexusTransformerBlock, NexusRMSNorm

class NexusModel(nn.Module):
    """
    Le modèle Transformer principal, sans la tête de classification.
    Orchestre l'embedding et l'empilement des blocs Transformer.
    """
    def __init__(self, config: ModelConfig):
        super().__init__()
        self.config = config
        
        # Couche d'embedding des tokens
        self.embed_tokens = NexusEmbedding(config)
        
        # Empilement des blocs Transformer
        self.layers = nn.ModuleList([NexusTransformerBlock(config) for _ in range(config.num_hidden_layers)])
        
        # Normalisation finale après les blocs
        self.norm = NexusRMSNorm(config.hidden_size, eps=config.rms_norm_eps)

    def forward(
        self, 
        input_ids: torch.LongTensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
    ) -> torch.Tensor:
        
        hidden_states = self.embed_tokens(input_ids)
        
        # Itération à travers les blocs Transformer
        for decoder_layer in self.layers:
            hidden_states = decoder_layer(
                hidden_states,
                attention_mask=attention_mask,
                position_ids=position_ids,
            )
            
        # Normalisation finale
        hidden_states = self.norm(hidden_states)
        
        return hidden_states

class NexusForCausalLM(nn.Module):
    """
    Le modèle Nexus complet pour la modélisation de langage causal (Causal LM).

    Cette classe intègre le `NexusModel` et ajoute une tête de classification
    pour produire les logits de prédiction du prochain token.
    """
    def __init__(self, config: ModelConfig):
        super().__init__()
        self.model = NexusModel(config)
        self.config = config

        # Tête de classification pour la modélisation du langage
        # Les poids peuvent être partagés avec les embeddings de token
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)

    def get_input_embeddings(self) -> nn.Module:
        return self.model.embed_tokens

    def set_input_embeddings(self, value: nn.Module):
        self.model.embed_tokens = value
        
    def get_output_embeddings(self) -> nn.Module:
        return self.lm_head

    def set_output_embeddings(self, new_embeddings: nn.Module):
        self.lm_head = new_embeddings

    def forward(
        self, 
        input_ids: torch.LongTensor,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        labels: Optional[torch.LongTensor] = None,
    ) -> Tuple[Optional[torch.Tensor], torch.Tensor]:
        """
        Passe avant complète, incluant le calcul de la perte si les `labels` sont fournis.
        """
        # 1. Obtenir les états cachés du modèle de base
        hidden_states = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
        )

        # 2. Calculer les logits
        logits = self.lm_head(hidden_states)

        # 3. Calculer la perte (si les labels sont fournis)
        loss = None
        if labels is not None:
            # Décaler les logits et les labels pour la prédiction du prochain token
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            
            # Utiliser CrossEntropyLoss pour calculer la perte
            loss_fct = nn.CrossEntropyLoss()
            shift_logits = shift_logits.view(-1, self.config.vocab_size)
            shift_labels = shift_labels.view(-1)
            loss = loss_fct(shift_logits, shift_labels)

        return loss, logits
