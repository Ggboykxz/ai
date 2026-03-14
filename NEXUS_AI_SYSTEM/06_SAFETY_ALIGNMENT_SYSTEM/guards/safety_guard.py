# --- NEXUS_AI_SYSTEM/06_SAFETY_ALIGNMENT_SYSTEM/safety_guard.py ---

from typing import Dict, Any

# Corrected to use relative imports for proper module structure.
from .content_moderation.sensitive_data_scanner import SensitiveDataScanner
from .risk_assessment.risk_assessor import CodeRiskAssessor

class SafetyGuard:
    """
    Acts as a final checkpoint before code modifications are applied.

    This class orchestrates multiple safety components—like the sensitive data
    scanner and the risk assessor—to make a final decision on whether a proposed
    code change is safe to proceed.
    """

    def __init__(self, risk_threshold: int = 10):
        """
        Initializes the Safety Guard with configurable thresholds.

        Args:
            risk_threshold (int): The maximum acceptable risk score for a code change.
                                  Changes exceeding this score will be rejected.
        """
        self.scanner = SensitiveDataScanner()
        self.assessor = CodeRiskAssessor()
        self.risk_threshold = risk_threshold

    def validate_code_change(self, code: str) -> Dict[str, Any]:
        """
        Validates a piece of code by running all safety checks.

        Args:
            code (str): The proposed new or modified code.

        Returns:
            Dict[str, Any]: A validation report containing the final decision ('approved', 
                            'rejected'), the risk score, and any specific findings.
        """
        print("\n--- Safety Guard: Validating code change... ---")
        
        # 1. Scan for sensitive data
        sensitive_data_findings = self.scanner.scan_content(code)
        
        # 2. Assess code risk
        # Re-initialize assessor for each run to reset state
        self.assessor = CodeRiskAssessor()
        risk_assessment = self.assessor.assess_code(code)
        risk_score = risk_assessment.get('risk_score', 0)

        # 3. Make a decision
        decision = 'approved'
        reasons = []

        if sensitive_data_findings:
            decision = 'rejected'
            reasons.append("Presence of sensitive data.")
        
        if risk_score > self.risk_threshold:
            decision = 'rejected'
            reasons.append(f"Code risk score ({risk_score}) exceeds threshold ({self.risk_threshold}).")

        report = {
            'decision': decision,
            'summary': ", ".join(reasons) if reasons else "All safety checks passed.",
            'risk_assessment': risk_assessment,
            'sensitive_data_scan': {'findings': sensitive_data_findings}
        }

        print(f"Validation complete. Decision: {decision.upper()}")
        return report

if __name__ == '__main__':
    print("--- Running Safety Guard Example ---")
    
    # Note: The following example code will not run directly without creating a proper
    # Python package structure (i.e., __init__.py files) and running as a module.
    # The code is provided for illustrative purposes.

    # To make this runnable, one would need to:
    # 1. Create __init__.py in all subdirectories.
    # 2. Run from the parent directory: python -m NEXUS_AI_SYSTEM.06_SAFETY_ALIGNMENT_SYSTEM.safety_guard

    print("\nThis __main__ block is for demonstration; it cannot be run directly.")

