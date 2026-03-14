import os
from NEXUS_AI_SYSTEM.utils.logging import Logger

class CodeAnalysisEngine:
    def __init__(self, main_engine):
        self.main_engine = main_engine
        self.logger = Logger("CodeAnalysisEngine")
        self.project_root = self.main_engine.project_root
        self.ignore_patterns = ['.git', '__pycache__', '.vscode', 'docs', 'tests']

    def analyze_codebase(self):
        """
        Analyse l'ensemble de la base de code pour identifier les fichiers Python pertinents.
        """
        self.logger.log("Starting codebase analysis...")
        python_files = self._find_python_files()
        self.logger.log(f"Found {len(python_files)} Python files to analyze.")

        # Pour l'instant, nous retournons simplement la liste des fichiers.
        # Les prochaines étapes impliqueront une analyse plus approfondie (AST, etc.).
        analysis_results = {"files_to_analyze": python_files}
        return analysis_results

    def _find_python_files(self):
        """
        Parcourt récursivement le projet pour trouver tous les fichiers .py,
        en ignorant les répertoires et fichiers spécifiés dans self.ignore_patterns.
        """
        python_files = []
        for root, dirs, files in os.walk(self.project_root):
            # Exclure les répertoires indésirables
            dirs[:] = [d for d in dirs if d not in self.ignore_patterns]

            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    python_files.append(full_path)
        return python_files
