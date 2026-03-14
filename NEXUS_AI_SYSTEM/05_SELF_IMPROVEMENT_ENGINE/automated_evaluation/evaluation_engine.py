import ast
from NEXUS_AI_SYSTEM.utils.logging import Logger

class EvaluationEngine:
    def __init__(self, main_engine):
        self.main_engine = main_engine
        self.logger = Logger("EvaluationEngine")

    def evaluate_changes(self, patch):
        """
        Évalue la validité des changements. 
        Pour l'instant, vérifie simplement la syntaxe du fichier modifié.

        Retourne True si l'évaluation est un succès, False sinon.
        """
        self.logger.log("Starting evaluation of changes...")

        if not patch or patch.get("action") != "REPLACE_FILE_CONTENT":
            self.logger.log("No valid patch to evaluate.")
            return True # Ne rien faire si le patch n'est pas valide

        file_path = patch.get("file_path")

        if not file_path.endswith(".py"):
            self.logger.log(f"Skipping syntax check for non-python file: {file_path}")
            return True

        return self._is_python_syntax_valid(file_path)

    def _is_python_syntax_valid(self, file_path):
        """Vérifie la syntaxe d'un fichier Python en essayant de le parser.
        Retourne True si la syntaxe est valide, False sinon.
        """
        self.logger.log(f"Checking Python syntax for: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            ast.parse(source_code)
            self.logger.log(f"Syntax check PASSED for: {file_path}")
            return True
        except SyntaxError as e:
            self.logger.log(f"Syntax check FAILED for: {file_path}", level="error")
            self.logger.log(f"Syntax error: {e}", level="error")
            return False
        except Exception as e:
            self.logger.log(f"An unexpected error occurred during syntax check for {file_path}: {e}", level="error")
            return False
