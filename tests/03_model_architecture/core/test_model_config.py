"""
Tests pour le module de configuration du modèle NEXUS-AI.
"""
import pytest
import json
from pathlib import Path
from NEXUS_AI_SYSTEM.03_MODEL_ARCHITECTURE.core.model_config import ModelConfig, NexusConfigFactory

def test_config_creation():
    """Teste la création d'une configuration de base."""
    config = ModelConfig(
        hidden_size=128,
        num_attention_heads=4,
        num_key_value_heads=2
    )
    assert config.hidden_size == 128
    assert config.num_attention_heads == 4
    assert config.num_key_value_heads == 2

def test_gqa_validation():
    """Teste la validation des contraintes pour GQA."""
    # Valide
    ModelConfig(hidden_size=128, num_attention_heads=8, num_key_value_heads=4)
    ModelConfig(hidden_size=128, num_attention_heads=8, num_key_value_heads=8) # MHA

    # Invalide
    with pytest.raises(ValueError, match="multiple"):
        ModelConfig(hidden_size=128, num_attention_heads=8, num_key_value_heads=3)

    with pytest.raises(ValueError, match="supérieur"):
        ModelConfig(hidden_size=128, num_attention_heads=4, num_key_value_heads=8)

def test_serialization(tmp_path: Path):
    """Teste la sauvegarde et le chargement (sérialisation)."""
    config = ModelConfig()
    file_path = tmp_path / "config.json"

    # Sauvegarde
    config.save(file_path)
    assert file_path.exists()

    # Chargement
    loaded_config = ModelConfig.load(file_path)
    assert loaded_config == config

    # Vérifie le contenu JSON
    with open(file_path, "r") as f:
        data = json.load(f)
    assert data["hidden_size"] == config.hidden_size

def test_nexus_config_factory():
    """Teste la factory de configurations prédéfinies."""
    nano_config = NexusConfigFactory.get_config("Nexus-7B")
    assert nano_config.hidden_size == 4096
    assert nano_config.num_hidden_layers == 32

    medium_config = NexusConfigFactory.get_config("Nexus-70B")
    assert medium_config.hidden_size == 8192
    assert medium_config.num_attention_heads == 64

    with pytest.raises(ValueError, match="non reconnue"):
        NexusConfigFactory.get_config("Nexus-Imaginary-Model")

def test_post_init_validation():
    """Teste la validation des dimensions dans __post_init__."""
    with pytest.raises(ValueError, match="divisible"):
        ModelConfig(hidden_size=129, num_attention_heads=8)


# Lancer les tests avec : pytest
