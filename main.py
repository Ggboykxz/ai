import yaml

def main():
    """Point d'entrée principal de l'application NEXUS-AI."""
    print("Initialisation du système NEXUS-AI...")

    # Charger la configuration
    with open("config/default.yaml", "r") as f:
        config = yaml.safe_load(f)

    print("Configuration chargée :")
    print(config)

if __name__ == "__main__":
    main()
