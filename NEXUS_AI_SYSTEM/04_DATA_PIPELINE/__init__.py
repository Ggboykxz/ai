
# --- NEXUS_AI_SYSTEM/04_DATA_PIPELINE/__init__.py ---

import torch
from torch.utils.data import Dataset
from typing import List

class CausalLMDataset(Dataset):
    """
    Un Dataset pour la modélisation de langage causal (Causal Language Modeling).

    Ce dataset prend une longue séquence de tokens et la divise en blocs
    de taille `block_size`. Chaque bloc devient un échantillon d'entraînement.

    Pour chaque échantillon, les `input_ids` et les `labels` sont créés.
    Par exemple, si block_size = 8 et les tokens sont [1, 2, 3, 4, 5, 6, 7, 8]:
    - input_ids: [1, 2, 3, 4, 5, 6, 7]
    - labels:    [2, 3, 4, 5, 6, 7, 8]
    Le modèle apprend ainsi à prédire le token suivant à chaque position.
    """
    def __init__(self, tokenized_data: List[int], block_size: int):
        """
        Initialise le dataset.

        Args:
            tokenized_data (List[int]): La liste complète des tokens du corpus.
            block_size (int): La longueur maximale d'une séquence pour le modèle.
        """
        self.block_size = block_size
        self.examples = []

        # Créer les exemples en découpant les données en blocs
        num_tokens = len(tokenized_data)
        for i in range(0, num_tokens - block_size + 1, block_size):
            chunk = tokenized_data[i : i + block_size]
            if len(chunk) == block_size:
                self.examples.append(chunk)

    def __len__(self) -> int:
        """
        Retourne le nombre total d'exemples (blocs) dans le dataset.
        """
        return len(self.examples)

    def __getitem__(self, idx: int) -> dict:
        """
        Récupère un exemple d'entraînement (input_ids et labels).

        Args:
            idx (int): L'index de l'exemple à récupérer.

        Returns:
            dict: Un dictionnaire contenant 'input_ids' et 'labels' sous forme de tenseurs.
        """
        block = self.examples[idx]
        
        # Les entrées sont tous les tokens sauf le dernier.
        # Les étiquettes sont tous les tokens sauf le premier.
        # Le modèle doit prédire le token suivant.
        input_ids = torch.tensor(block[:-1], dtype=torch.long)
        labels = torch.tensor(block[1:], dtype=torch.long)
        
        # Pour la fonction de perte CrossEntropy, les labels et les inputs doivent correspondre
        # à la sortie des logits. Notre modèle décale déjà les logits et les labels.
        # Donc, on peut fournir les tenseurs complets, et le décalage se fera
        # dans la boucle d'entraînement ou la fonction forward du modèle.
        # Pour coller à l'implémentation de la perte dans `NexusForCausalLM`,
        # nous devons nous assurer que le décalage est bien géré.
        
        # Le forward de `NexusForCausalLM` fait: 
        #   shift_logits = logits[..., :-1, :]
        #   shift_labels = labels[..., 1:]
        # Si nous passons un block complet comme `labels`, le `labels[..., 1:]` 
        # créera la bonne cible. Donc, nous pouvons passer le bloc entier pour les deux.
        
        full_block = torch.tensor(block, dtype=torch.long)

        return {
            "input_ids": full_block,
            "labels": full_block
        }

# Note sur l'implémentation de __getitem__:
# La méthode forward de `NexusForCausalLM` est conçue pour gérer le décalage elle-même :
# `shift_logits = logits[..., :-1, :].contiguous()`
# `shift_labels = labels[..., 1:].contiguous()`
# Cela signifie que si `input_ids` a une longueur L, `logits` aura une longueur L.
# `shift_logits` aura la longueur L-1 (tous sauf le dernier logit).
# `shift_labels` doit aussi avoir la longueur L-1.
# Si nous passons le `full_block` de longueur L comme `labels`, `labels[..., 1:]` créera
# un tenseur de longueur L-1, ce qui est correct.
# C'est une convention courante dans les librairies comme Hugging Face Transformers.
