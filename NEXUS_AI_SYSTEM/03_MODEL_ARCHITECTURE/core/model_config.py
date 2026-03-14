"""
NEXUS-AI — Architecture du Modèle

Ce fichier définit la configuration de base pour tous les modèles NEXUS-AI.
Il utilise des dataclasses pour assurer la cohérence, la validation et la
reproductibilité des hyperparamètres du modèle.
"""
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Any, Union

@dataclass
class ModelConfig:
    """
    Configuration de base pour les modèles Transformer de NEXUS-AI.

    Attributes:
        vocab_size (int): Taille du vocabulaire.
        hidden_size (int): Dimension de la couche cachée.
        num_hidden_layers (int): Nombre de couches Transformer.
        num_attention_heads (int): Nombre de têtes d'attention (pour GQA, c'est le nombre de têtes de query).
        num_key_value_heads (int): Nombre de têtes pour Key/Value (doit être <= num_attention_heads).
        ffn_hidden_size (int): Dimension de la couche FFN. Souvent un multiple de hidden_size.
        max_position_embeddings (int): Longueur de contexte maximale.
        rope_theta (float): Base pour l'encodage positionnel RoPE.
        norm_eps (float): Epsilon pour la normalisation (RMSNorm).
        use_flash_attn_v3 (bool): Utiliser FlashAttention v3 si disponible.
        tie_word_embeddings (bool): Partager les poids entre l'embedding et la tête de sortie.
    """
    # --- Architecture Dimensions ---
    vocab_size: int = 102400
    hidden_size: int = 4096
    num_hidden_layers: int = 32

    # --- Attention ---
    num_attention_heads: int = 32
    num_key_value_heads: int = 8  # Pour GQA
    rope_theta: float = 10000.0
    use_flash_attn_v3: bool = True

    # --- Feed-Forward Network ---
    ffn_hidden_size: int = 14336

    # --- Positional Embeddings & Context ---
    max_position_embeddings: int = 32768

    # --- Normalization & Output ---
    norm_eps: float = 1e-6
    tie_word_embeddings: bool = True

    def __post_init__(self):
        """Validation post-initialisation."""
        if self.hidden_size % self.num_attention_heads != 0:
            raise ValueError(
                f"hidden_size ({self.hidden_size}) doit être divisible par "
                f"num_attention_heads ({self.num_attention_heads})"
            )
        if self.num_key_value_heads > self.num_attention_heads:
            raise ValueError(
                f"num_key_value_heads ({self.num_key_value_heads}) ne peut pas "
                f"être supérieur à num_attention_heads ({self.num_attention_heads})"
            )
        if self.num_attention_heads % self.num_key_value_heads != 0:
            raise ValueError(
                "Le nombre de têtes d\'attention doit être un multiple "
                "du nombre de têtes key/value pour GQA."
            )

    def to_dict(self) -> Dict[str, Any]:
        """Sérialise la configuration en dictionnaire."""
        return asdict(self)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "ModelConfig":
        """Crée une instance de ModelConfig à partir d'un dictionnaire."""
        return cls(**config_dict)

    def save(self, path: Union[str, Path]):
        """Sauvegarde la configuration dans un fichier JSON."""
        config_path = Path(path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, path: Union[str, Path]) -> "ModelConfig":
        """Charge la configuration depuis un fichier JSON."""
        with open(path, "r", encoding="utf-8") as f:
            config_dict = json.load(f)
        return cls.from_dict(config_dict)

# --- Usine de Configurations Prédéfinies ---

class NexusConfigFactory:
    """Crée des configurations de modèle standardisées."""

    @staticmethod
    def get_config(name: str) -> ModelConfig:
        """
        Récupère une configuration prédéfinie par son nom.
        Exemples: "Nexus-7B", "Nexus-70B"
        """
        configs = {
            "Nexus-7B": NexusConfigFactory.NexusNano(),
            "Nexus-13B": NexusConfigFactory.NexusSmall(),
            "Nexus-70B": NexusConfigFactory.NexusMedium(),
            "Nexus-200B": NexusConfigFactory.NexusLarge(),
        }
        config = configs.get(name)
        if config is None:
            raise ValueError(f"Configuration '{name}' non reconnue. "
                             f"Options valides : {list(configs.keys())}")
        return config

    @staticmethod
    def NexusNano() -> ModelConfig:
        """Configuration ~7B paramètres (style Llama 3 8B)."""
        return ModelConfig(
            hidden_size=4096,
            num_hidden_layers=32,
            num_attention_heads=32,
            num_key_value_heads=8,
            ffn_hidden_size=14336,
            rope_theta=500000.0,
        )

    @staticmethod
    def NexusSmall() -> ModelConfig:
        """Configuration ~13B paramètres."""
        return ModelConfig(
            hidden_size=5120,
            num_hidden_layers=40,
            num_attention_heads=40,
            num_key_value_heads=10,
            ffn_hidden_size=17280,
            rope_theta=500000.0,
        )

    @staticmethod
    def NexusMedium() -> ModelConfig:
        """Configuration ~70B paramètres (style Llama 3 70B)."""
        return ModelConfig(
            hidden_size=8192,
            num_hidden_layers=80,
            num_attention_heads=64,
            num_key_value_heads=8,
            ffn_hidden_size=28672,
            rope_theta=500000.0,
        )

    @staticmethod
    def NexusLarge() -> ModelConfig:
        """Configuration ~200B+ paramètres."""
        return ModelConfig(
            hidden_size=12288,
            num_hidden_layers=96,
            num_attention_heads=96,
            num_key_value_heads=12,
            ffn_hidden_size=40960,
            rope_theta=1000000.0,
        )

if __name__ == '__main__':
    # Exemple d'utilisation
    print("--- Configuration Nano (7B) ---")
    config_7b = NexusConfigFactory.get_config("Nexus-7B")
    print(config_7b)

    # Sauvegarde et chargement
    save_path = Path("./temp_config.json")
    config_7b.save(save_path)
    print(f"\nConfiguration sauvegardée dans {save_path}")

    loaded_config = ModelConfig.load(save_path)
    print("\nConfiguration chargée :")
    print(loaded_config)
    assert loaded_config == config_7b

    save_path.unlink() # Nettoyage
    print(f"\nFichier temporaire {save_path} supprimé.")
