{ pkgs, ... }: {
  # Utiliser le channel unstable pour avoir accès aux paquets les plus récents
  channel = "unstable";

  # Paquets Nix à installer dans l'environnement
  packages = [
    # Créer un environnement Python avec les paquets spécifiés
    (pkgs.python311.withPackages (ps: [
      ps.flask
      ps.streamlit
    ]))
  ];

  # Extensions VS Code à installer
  idx = {
    extensions = [
      "ms-python.python"
      "ms-toolsai.jupyter"
    ];

    # Commandes à exécuter lors du cycle de vie de l'espace de travail
    workspace = {
      # Les dépendances Python sont maintenant gérées directement par Nix,
      # donc la commande `pip install` n'est plus nécessaire.
      onCreate = {};
      
      # Au démarrage de l'espace de travail, lancer l'application Streamlit
      onStart = {
        start-app = "streamlit run NEXUS_AI_SYSTEM/09_WEB_INTERFACE/main.py";
      };
    };
    previews = {
        enable = true;
        previews = {
            web = {
                command = ["streamlit" "run" "NEXUS_AI_SYSTEM/09_WEB_INTERFACE/main.py" "--server.port" "$PORT"];
                manager = "web";
            };
        };
    };
  };
}
