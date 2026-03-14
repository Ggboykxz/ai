from NEXUS_AI_SYSTEM.utils.logging import Logger

class RewritingEngine:
    def __init__(self, main_engine):
        self.main_engine = main_engine
        self.logger = Logger("RewritingEngine")

    def apply_changes(self, proposed_solution):
        """
        Applique les changements proposés à la base de code.
        Pour l'instant, gère une action simple : 'REPLACE_FILE_CONTENT'.

        Retourne un "patch" qui contient les informations nécessaires pour un rollback.
        """
        action = proposed_solution.get("action")
        if action != "REPLACE_FILE_CONTENT":
            self.logger.log(f"Action '{action}' not supported. No changes applied.")
            return None

        file_path = proposed_solution.get("file_path")
        new_content = proposed_solution.get("new_content")

        if not all([file_path, new_content is not None]):
            self.logger.log("Invalid proposal for REPLACE_FILE_CONTENT. Missing parameters.", level="error")
            return None
        
        try:
            # Sauvegarder le contenu original pour le rollback
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Appliquer le nouveau contenu
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            self.logger.log(f"Successfully rewrote file: {file_path}")

            # Le patch contient tout ce qui est nécessaire pour annuler l'opération
            patch = {
                "action": "REPLACE_FILE_CONTENT",
                "file_path": file_path,
                "original_content": original_content
            }
            return patch

        except Exception as e:
            self.logger.log(f"Failed to rewrite file {file_path}: {e}", level="error")
            return None

    def rollback_changes(self, patch):
        """
        Annule les changements décrits dans le patch.
        """
        self.logger.log(f"Rolling back changes for file: {patch['file_path']}")
        action = patch.get("action")
        if action != "REPLACE_FILE_CONTENT":
            self.logger.log(f"Rollback for action '{action}' not supported.", level="error")
            return

        file_path = patch.get("file_path")
        original_content = patch.get("original_content")

        try:
            # Restaurer le contenu original
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            self.logger.log(f"Successfully rolled back file: {file_path}")
        except Exception as e:
            self.logger.log(f"Failed to rollback file {file_path}: {e}", level="error")
