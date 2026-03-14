from NEXUS_AI_SYSTEM.utils.logging import Logger
from NEXUS_AI_SYSTEM.05_SELF_IMPROVEMENT_ENGINE.code_analyzer.code_analysis_engine import CodeAnalysisEngine
from NEXUS_AI_SYSTEM.05_SELF_IMPROVEMENT_ENGINE.synthesis.synthesis_engine import SynthesisEngine
from NEXUS_AI_SYSTEM.05_SELF_IMPROVEMENT_ENGINE.rewriting.rewriting_engine import RewritingEngine
from NEXUS_AI_SYSTEM.05_SELF_IMPROVEMENT_ENGINE.automated_evaluation.evaluation_engine import EvaluationEngine
from NEXUS_AI_SYSTEM.05_SELF_IMPROVEMENT_ENGINE.safe_integration.integration_engine import IntegrationEngine

class SelfImprovementEngine:
    def __init__(self, main_engine):
        self.main_engine = main_engine
        self.project_root = "."
        self.logger = Logger("SelfImprovementEngine")
        self.code_analyzer = CodeAnalysisEngine(self)
        self.synthesis_engine = SynthesisEngine(self)
        self.rewriting_engine = RewritingEngine(self)
        self.evaluation_engine = EvaluationEngine(self)
        self.integration_engine = IntegrationEngine(self)
        self.improvement_cycle = 0

    def run_improvement_cycle(self):
        self.improvement_cycle += 1
        self.logger.log(f"--- Starting Self-Improvement Cycle #{self.improvement_cycle} ---")

        # 1. Analyse
        analysis_results = self.code_analyzer.analyze_codebase()
        if not analysis_results or not analysis_results.get("files_to_analyze"):
            self.logger.log("Analysis yielded no files to process. Ending cycle.")
            return

        # 2. Synthèse avec le LLM
        proposed_solution = self.synthesis_engine.synthesize_solution(analysis_results)
        if not proposed_solution:
            self.logger.log("Synthesis failed to produce a solution. Ending cycle.")
            return

        # 3. Réécriture
        patch = self.rewriting_engine.apply_changes(proposed_solution)

        if patch:
            # 4. Évaluation
            is_safe = self.evaluation_engine.evaluate_changes(patch)

            if is_safe:
                self.logger.log("Evaluation successful. Changes are safe.")
                # 5. Intégration
                self.integration_engine.integrate_changes(patch, self.improvement_cycle)
            else:
                self.logger.log("Evaluation failed. Rolling back changes.", level="warning")
                # 6. Rollback
                self.rewriting_engine.rollback_changes(patch)
        
        self.logger.log(f"--- Finished Self-Improvement Cycle #{self.improvement_cycle} ---")
