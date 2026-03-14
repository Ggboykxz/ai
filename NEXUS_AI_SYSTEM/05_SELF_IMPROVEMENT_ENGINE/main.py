import time
from NEXUS_AI_SYSTEM.self_improvement_engine.code_analyzer.code_analysis_engine import CodeAnalysisEngine
from NEXUS_AI_SYSTEM.self_improvement_engine.synthesis.synthesis_engine import SynthesisEngine
from NEXUS_AI_SYSTEM.self_improvement_engine.rewriting.rewriting_engine import RewritingEngine
from NEXUS_AI_SYSTEM.self_improvement_engine.automated_evaluation.evaluation_engine import EvaluationEngine
from NEXUS_AI_SYSTEM.self_improvement_engine.safe_integration.integration_engine import IntegrationEngine
from NEXUS_AI_SYSTEM.utils.logging import Logger

class SelfImprovementEngine:
    def __init__(self, project_root):
        self.project_root = project_root
        self.logger = Logger("SelfImprovementEngine")
        self.code_analyzer = CodeAnalysisEngine(self)
        self.synthesis_engine = SynthesisEngine(self)
        self.rewriting_engine = RewritingEngine(self)
        self.evaluation_engine = EvaluationEngine(self)
        self.integration_engine = IntegrationEngine(self)
        self.improvement_cycles = 0

    def run_improvement_cycle(self):
        '''
        Exécute un cycle complet d'auto-amélioration.
        1. Analyse le code pour identifier les axes d'amélioration.
        2. Synthétise une solution (nouveau code).
        3. Réécrit le code avec la solution proposée.
        4. Évalue la nouvelle version.
        5. Intègre la solution si l'évaluation est positive.
        '''
        self.improvement_cycles += 1
        self.logger.log(f"--- Starting Self-Improvement Cycle #{self.improvement_cycles} ---")

        try:
            # 1. Analyse
            analysis_results = self.code_analyzer.analyze_codebase()
            if not analysis_results:
                self.logger.log("Analysis did not yield any improvement targets. Ending cycle.")
                return

            # 2. Synthèse
            proposed_solution = self.synthesis_engine.synthesize_solution(analysis_results)
            if not proposed_solution:
                self.logger.log("Synthesis did not produce a viable solution. Ending cycle.")
                return

            # 3. Réécriture
            patch = self.rewriting_engine.apply_changes(proposed_solution)
            if not patch:
                self.logger.log("Code rewriting failed. Ending cycle.")
                return

            # 4. Évaluation
            evaluation_passed = self.evaluation_engine.evaluate_changes(patch)
            if not evaluation_passed:
                self.logger.log("Evaluation failed. Rolling back changes.")
                self.rewriting_engine.rollback_changes(patch)
                return

            # 5. Intégration
            self.integration_engine.integrate_changes(patch, self.improvement_cycles)
            self.logger.log(f"--- Successfully Completed Self-Improvement Cycle #{self.improvement_cycles} ---")

        except Exception as e:
            self.logger.log(f"Error during improvement cycle: {e}", level="error")
            # En cas d'erreur, on pourrait envisager un rollback plus robuste ici.

    def start(self, interval_seconds=3600):
        '''Démarre la boucle d'auto-amélioration continue.'''
        self.logger.log("Self-Improvement Engine starting...")
        while True:
            self.run_improvement_cycle()
            self.logger.log(f"Next improvement cycle in {interval_seconds} seconds.")
            time.sleep(interval_seconds)

if __name__ == '__main__':
    # Ceci est un exemple de la façon dont le moteur pourrait être démarré.
    # Le point d'entrée réel sera probablement dans le main.py racine du projet.
    engine = SelfImprovementEngine(project_root=".")
    engine.start(interval_seconds=60) # Intervalle court pour le débogage
