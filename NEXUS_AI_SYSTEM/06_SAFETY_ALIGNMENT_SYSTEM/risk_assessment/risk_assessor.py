# --- NEXUS_AI_SYSTEM/06_SAFETY_ALIGNMENT_SYSTEM/risk_assessment/risk_assessor.py ---

import ast
from typing import List, Dict, Set

class CodeRiskAssessor(ast.NodeVisitor):
    """
    Assesses the potential risk of a Python code snippet by analyzing its AST.

    This visitor traverses the AST to find imports and function calls that are
    pre-defined as potentially high-risk, such as filesystem operations, 
    network requests, or subprocess execution.
    """

    # A simple classification of risky modules and functions.
    # A more advanced system would have weighted scores and more context.
    RISKY_MODULES = {
        'os': 3,
        'subprocess': 5,
        'shutil': 4,
        'requests': 2,
        'socket': 4,
        'http': 2,
        'urllib': 2,
        'ftplib': 2,
        'eval': 10, # eval is extremely risky
        'exec': 10  # exec is also extremely risky
    }

    def __init__(self):
        self.findings: List[Dict] = []
        self.imported_modules: Set[str] = set()
        self.risk_score: int = 0

    def visit_Import(self, node: ast.Import):
        """Checks for imports of risky modules."""
        for alias in node.names:
            module_name = alias.name
            if module_name in self.RISKY_MODULES:
                risk = self.RISKY_MODULES[module_name]
                self.risk_score += risk
                self.findings.append({
                    'type': 'Risky Import',
                    'module': module_name,
                    'line': node.lineno,
                    'risk_level': risk,
                    'description': f"Import of potentially risky module '{module_name}' detected."
                })
            self.imported_modules.add(module_name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Checks for `from ... import ...` of risky modules."""
        module_name = node.module
        if module_name in self.RISKY_MODULES:
            risk = self.RISKY_MODULES[module_name]
            self.risk_score += risk
            self.findings.append({
                'type': 'Risky Import From',
                'module': module_name,
                'line': node.lineno,
                'risk_level': risk,
                'description': f"Import from potentially risky module '{module_name}' detected."
            })
            self.imported_modules.add(module_name)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        """
        Checks for calls to globally risky functions like eval() and exec().
        """
        # This handles direct calls like `eval(...)`
        if isinstance(node.func, ast.Name) and node.func.id in ('eval', 'exec'):
            func_name = node.func.id
            risk = self.RISKY_MODULES[func_name]
            self.risk_score += risk
            self.findings.append({
                'type': 'High-Risk Function Call',
                'function': func_name,
                'line': node.lineno,
                'risk_level': risk,
                'description': f"Direct call to built-in, high-risk function '{func_name}'."
            })
        self.generic_visit(node)

    def assess_code(self, source_code: str) -> Dict:
        """
        Parses the code, runs the visitor, and returns a risk assessment report.

        Args:
            source_code (str): The Python code to analyze.

        Returns:
            Dict: A dictionary containing the total risk score and a list of findings.
        """
        print("\n--- Assessing code risk... ---")
        try:
            tree = ast.parse(source_code)
            self.visit(tree)
        except SyntaxError as e:
            return {
                'risk_score': -1, # Indicates a parsing error
                'findings': [],
                'error': f"Syntax error in code: {e}"
            }
        
        report = {
            'risk_score': self.risk_score,
            'findings': self.findings
        }
        print(f"Risk assessment complete. Score: {self.risk_score}")
        return report

if __name__ == '__main__':
    print("--- Running Code Risk Assessor Example ---")

    # Example code with varying levels of risk
    risky_code = '''
    import os
    import subprocess
    import requests # For making API calls

    # This function is dangerous
    def run_command(cmd):
        # High risk: executes arbitrary shell commands
        subprocess.run(cmd, shell=True)

    # This function is also risky
    def delete_file(path):
        os.remove(path)

    # This is less risky but still involves network I/O
    def get_data(url):
        response = requests.get(url)
        return response.text

    # Extremely high risk
    user_input = "__import__('os').system('echo hacked')"
    eval(user_input)
    '''

    assessor = CodeRiskAssessor()
    assessment_report = assessor.assess_code(risky_code)

    print("\n--- Risk Assessment Report ---")
    print(f"Total Risk Score: {assessment_report['risk_score']}")
    if assessment_report['findings']:
        for f in assessment_report['findings']:
            print(f"- [Line {f['line']}] {f['description']} (Risk: {f['risk_level']})")
    else:
        print("No specific risks detected.")
