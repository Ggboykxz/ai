{ pkgs, ... }: {
  # Utiliser le channel unstable pour avoir accès aux paquets les plus récents
  channel = "unstable";

  # Paquets Nix à installer dans l'environnement
  packages = [
    pkgs.python311
    pkgs.pip
  ];

  # Extensions VS Code à installer
  idx = {
    extensions = [
      "ms-python.python"
      "ms-toolsai.jupyter"
    ];

    # Commandes à exécuter lors du cycle de vie de l'espace de travail
    workspace = {
      # À la création de l'espace de travail, installer les dépendances Python
      onCreate = {
        install-deps = "pip install -r requirements.txt";
      };
    };
  };
}
