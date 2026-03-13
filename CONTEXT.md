# NEXUS-AI — CONTEXT.md
Dernière mise à jour : 2024-07-30 10:00:00
Version : 0.1.0

## État actuel du projet
Initialisation du projet NEXUS-AI. Le socle du projet vient d'être défini par la mise en place des règles de développement (airules.md) et la configuration de l'environnement Nix (dev.nix). Le fichier de contexte est maintenant en place. Aucun module fonctionnel n'existe.

## Architecture actuelle
- `CONTEXT.md`: (Ce fichier) Fichier de contexte central et mémoire vivante du projet.
- `README.md`: Fichier d'accueil général du projet.
- `.idx/dev.nix`: Fichier de configuration de l'environnement de développement Nix pour Firebase Studio.
- `.idx/airules.md`: Fichier contenant les règles pour l'assistant IA (NEXUS-AI Dev System).

## Modules implémentés
- [⬜] Initialisation de la structure du projet et des règles de gouvernance.

## Dernières modifications
- 2024-07-30 10:00:00 | CONTEXT.md | feat: Initialisation du fichier de contexte du projet.

## Décisions techniques prises
- **Assistant IA**: Utilisation du "NEXUS-AI Dev System" avec un ensemble de règles strictes pour garantir la qualité et la cohérence du code.
- **Environnement**: Utilisation de Nix (`.idx/dev.nix`) pour un environnement de développement déclaratif et reproductible.
- **Contrôle de version**: Adoption du standard Conventional Commits 1.0.0.

## Dépendances
- Aucune pour le moment.

## Variables d'environnement requises
- Aucune pour le moment.

## Commandes importantes
- `git init`: Pour initialiser le dépôt.
- `git commit`: Pour enregistrer les modifications en respectant la convention.

## Problèmes connus / TODO critiques
- Le dépôt Git n'est pas encore initialisé.
- Le langage de programmation principal et les dépendances de base doivent être définis dans `.idx/dev.nix`.

## Prochaine étape
Initialiser le dépôt `git` et effectuer le premier commit avec les fichiers de structure (`CONTEXT.md`, `README.md`, `.idx/dev.nix`, `.idx/airules.md`).