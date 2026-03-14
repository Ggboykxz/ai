
# --- NEXUS_AI_SYSTEM/03_MODEL_ARCHITECTURE/model.py ---

import torch
from torch import nn

from .core.model_config import ModelConfig
from .transformer.transformer_block import NexusTransformerBlock

class NexusForCausalLM(nn.Module):
    """
    L'architecture principale du modèle Nexus, assemblant les différents composants.
    """
    def __init__(self, config: ModelConfig):
        super().__init__()
        self.config = config

        # Couche d'embedding des tokens
        self.token_embeddings = nn.Embedding(config.vocab_size, config.hidden_size)

        # Blocs Transformer empilés
        self.transformer_blocks = nn.ModuleList(
            [NexusTransformerBlock(config) for _ in range(config.num_hidden_layers)]
        )

        # Tête de modélisation du langage (prédit le prochain token)
        self.lm_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)

    def forward(self, input_ids: torch.Tensor, labels: torch.Tensor = None):
        """
        Passe avant du modèle.

        Args:
            input_ids (torch.Tensor): Les IDs des tokens d'entrée (batch_size, seq_length).
            labels (torch.Tensor, optional): Les IDs des tokens cibles pour le calcul de la perte (batch_size, seq_length).

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: La perte (si labels est fourni) et les logits.
        """
        batch_size, seq_length = input_ids.shape
        device = input_ids.device

        # 1. Obtenir les embeddings
        hidden_states = self.token_embeddings(input_ids)

        # 2. Passer à travers les blocs Transformer
        for block in self.transformer_blocks:
            hidden_states = block(hidden_states)

        # 3. Calculer les logits avec la tête de modélisation
        logits = self.lm_head(hidden_states)

        # 4. Calculer la perte si les étiquettes sont fournies
        loss = None
        if labels is not None:
            # Aplatir les logits et les étiquettes pour le calcul de la perte
            # On veut prédire le prochain token, donc on décale les logits et les labels
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()

            loss_fct = nn.CrossEntropyLoss()
            loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))

        return loss, logits
    
    def count_parameters(self):
        """Compte le nombre total de paramètres dans le modèle."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    @torch.no_grad()
    def generate(self, input_ids: torch.Tensor, max_new_tokens: int, temperature: float = 1.0):
        """
        Génère une séquence de tokens de manière autorégressive.

        Args:
            input_ids (torch.Tensor): Le prompt d'entrée (batch_size, seq_length).
            max_new_tokens (int): Le nombre maximum de nouveaux tokens à générer.
            temperature (float): Contrôle le caractère aléatoire. 1.0 = pas de changement.
                                 < 1.0 rend la sortie plus déterministe (greedy).
                                 > 1.0 la rend plus aléatoire.

        Returns:
            torch.Tensor: La séquence de tokens complétée.
        """
        self.eval() # Mettre le modèle en mode évaluation
        generated_ids = input_ids

        for _ in range(max_new_tokens):
            # Ne considérer que la fenêtre de contexte maximale
            input_ids_cond = generated_ids[:, -self.config.block_size:]

            # Passe avant pour obtenir les logits pour le dernier token
            _, logits = self(input_ids_cond)
            last_token_logits = logits[:, -1, :] / temperature

            # Appliquer softmax pour obtenir les probabilités
            probs = torch.nn.functional.softmax(last_token_logits, dim=-1)

            # Échantillonner le prochain token
            next_token_id = torch.multinomial(probs, num_samples=1)

            # Ajouter le nouveau token à la séquence générée
            generated_ids = torch.cat((generated_ids, next_token_id), dim=1)

        self.train() # Remettre le modèle en mode entraînement
        return generated_ids
