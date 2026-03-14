from NEXUS_AI_SYSTEM.utils.logging import Logger
import json

class SynthesisEngine:
    def __init__(self, main_engine):
        self.main_engine = main_engine
        self.logger = Logger("SynthesisEngine")

    def synthesize_solution(self, analysis_results):
        self.logger.log("Starting solution synthesis with LLM...")
        files_to_analyze = analysis_results.get("files_to_analyze", [])
        if not files_to_analyze:
            self.logger.log("No files to analyze. Synthesis cannot proceed.")
            return None

        file_contents = self._read_file_contents(files_to_analyze)

        # Pour cette simulation, nous nous concentrons sur un fichier spécifique
        target_file = "NEXUS_AI_SYSTEM/05_SELF_IMPROVEMENT_ENGINE/rewriting/rewriting_engine.py"
        if target_file not in file_contents:
            self.logger.log(f"Target file {target_file} not found in analysis. Cannot synthesize.", level="warning")
            return None
        
        # 1. Construire le prompt pour le LLM
        prompt = self._build_llm_prompt(target_file, file_contents[target_file])

        # 2. Appeler le LLM (simulé pour l'instant)
        llm_response_str = self._call_llm_mock(prompt)
        
        # 3. Parser et valider la réponse du LLM
        try:
            llm_response = json.loads(llm_response_str)
            # ... (ajouter une validation plus robuste ici) ...
        except json.JSONDecodeError as e:
            self.logger.log(f"Failed to decode LLM response: {e}", level="error")
            return None

        # 4. Transformer la réponse du LLM en une proposition d'action
        proposed_solution = {
            "action": "REPLACE_FILE_CONTENT",
            "file_path": llm_response.get("file_path"),
            "new_content": llm_response.get("improved_code"),
            "reason": llm_response.get("explanation")
        }

        self.logger.log(f"Successfully synthesized a proposal from LLM: {proposed_solution['reason']}")
        return proposed_solution

    def _read_file_contents(self, file_paths):
        contents = {}
        for path in file_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    contents[path] = f.read()
            except Exception as e:
                self.logger.log(f"Error reading file {path}: {e}", level="error")
        return contents

    def _build_llm_prompt(self, file_path, file_content):
        """ Prépare le prompt pour le LLM. """
        return f"""Analyze the following Python code from the file '{file_path}'.

Your task is to improve this code by adding more detailed logging to the `apply_changes` and `rollback_changes` methods. 
This will help in tracing the engine's operations more effectively.

The response should be a JSON object with the following keys:
- "file_path": The full path of the file to modify.
- "improved_code": The complete, new source code for the file, including your improvements.
- "explanation": A brief explanation of the changes you made.

Here is the code:

```python
{file_content}
```
"""

    def _call_llm_mock(self, prompt):
        """ Simule un appel à un LLM. Retourne une réponse au format JSON string. """
        self.logger.log("Simulating a call to a Language Model...")
        
        # La réponse simulée améliore le logging dans RewritingEngine
        improved_code = '''from NEXUS_AI_SYSTEM.utils.logging import Logger

class RewritingEngine:
    def __init__(self, main_engine):
        self.main_engine = main_engine
        self.logger = Logger("RewritingEngine")

    def apply_changes(self, proposed_solution):
        self.logger.log("Attempting to apply changes...")
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
            self.logger.log(f"Reading original content of {file_path} for rollback.")
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            self.logger.log(f"Writing new content to {file_path}.")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            self.logger.log(f"Successfully rewrote file: {file_path}")

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
        self.logger.log(f"Attempting to roll back changes for file: {patch.get('file_path')}")
        action = patch.get("action")
        if action != "REPLACE_FILE_CONTENT":
            self.logger.log(f"Rollback for action '{action}' not supported.", level="error")
            return

        file_path = patch.get("file_path")
        original_content = patch.get("original_content")

        try:
            self.logger.log(f"Restoring original content to {file_path}.")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            self.logger.log(f"Successfully rolled back file: {file_path}")
        except Exception as e:
            self.logger.log(f"Failed to rollback file {file_path}: {e}", level="error")'''

        response = {
            "file_path": "NEXUS_AI_SYSTEM/05_SELF_IMPROVEMENT_ENGINE/rewriting/rewriting_engine.py",
            "improved_code": improved_code,
            "explanation": "Added more detailed logging to the `apply_changes` and `rollback_changes` methods to improve traceability of file operations."
        }

        return json.dumps(response)
