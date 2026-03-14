# --- NEXUS_AI_SYSTEM/05_SELF_IMPROVEMENT_ENGINE/code_analysis/ast_analyzer.py ---

import ast
from collections import defaultdict
import json
from typing import List, Dict, Any, Set

class ASTAnalyzer:
    """
    Analyzes a given Python source code using Abstract Syntax Trees (AST).

    This class provides functionalities to:
    - Parse source code into an AST.
    - Count different types of AST nodes (e.g., functions, classes, loops).
    - Extract names of defined functions, classes, and imported modules.
    - Statically analyze code without executing it.
    """
    def __init__(self, source_code: str):
        """
        Initializes the analyzer with the source code.

        Args:
            source_code (str): The Python source code to analyze.
        
        Raises:
            SyntaxError: If the source code is not valid Python code.
        """
        self.source_code = source_code
        self.tree: ast.Module = ast.parse(source_code)
        self.stats: Dict[str, int] = defaultdict(int)
        self.imports: Set[str] = set()
        self.functions: List[Dict[str, Any]] = []
        self.classes: List[Dict[str, Any]] = []

    def analyze(self) -> None:
        """
        Performs a full analysis of the AST.
        
        It traverses the AST and populates the internal statistics.
        This method must be called before getting a report.
        """
        self._traverse(self.tree)
        print("AST Analysis complete.")

    def _traverse(self, node: ast.AST) -> None:
        """
        Recursively traverses the AST nodes to gather statistics.
        """
        node_type = type(node).__name__
        self.stats[node_type] += 1

        if isinstance(node, ast.Import):
            for alias in node.names:
                self.imports.add(alias.name)
        
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                self.imports.add(node.module)

        elif isinstance(node, ast.FunctionDef):
            self.functions.append(self._get_function_details(node))

        elif isinstance(node, ast.ClassDef):
            self.classes.append(self._get_class_details(node))

        for child in ast.iter_child_nodes(node):
            self._traverse(child)
    
    def _get_function_details(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """ Extracts details from a FunctionDef node. """
        return {
            "name": node.name,
            "args": [arg.arg for arg in node.args.args],
            "lineno": node.lineno,
            "end_lineno": getattr(node, 'end_lineno', node.lineno) # end_lineno requires Python 3.8+
        }

    def _get_class_details(self, node: ast.ClassDef) -> Dict[str, Any]:
        """ Extracts details from a ClassDef node. """
        return {
            "name": node.name,
            "bases": [base.id for base in node.bases if isinstance(base, ast.Name)],
            "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
            "lineno": node.lineno,
            "end_lineno": getattr(node, 'end_lineno', node.lineno)
        }

    def get_report(self, as_json: bool = False) -> str:
        """
        Returns a formatted report of the analysis.

        Args:
            as_json (bool): If True, returns the report in JSON format.
        
        Returns:
            str: A formatted string or JSON string of the analysis report.
        """
        report_data = {
            "node_counts": dict(self.stats),
            "imports": sorted(list(self.imports)),
            "defined_classes": self.classes,
            "defined_functions": self.functions,
            "total_nodes": sum(self.stats.values()),
        }
        if as_json:
            return json.dumps(report_data, indent=2)
        
        report_str = "--- AST Analysis Report ---\n"
        report_str += f"Total Nodes: {report_data['total_nodes']}\n"
        
        report_str += "\n[Node Counts]\n"
        for node_type, count in sorted(self.stats.items()):
            report_str += f"- {node_type}: {count}\n"
        
        report_str += "\n[Imports]\n"
        if report_data["imports"]:
            for imp in report_data["imports"]:
                report_str += f"- {imp}\n"
        else:
            report_str += "No imports found.\n"

        report_str += "\n[Classes]\n"
        if self.classes:
            for cls in self.classes:
                report_str += f"- {cls['name']} (lines {cls['lineno']}-{cls['end_lineno']})\n"
        else:
            report_str += "No classes found.\n"

        report_str += "\n[Functions]\n"
        if self.functions:
            for func in self.functions:
                report_str += f"- {func['name']} (lines {func['lineno']}-{func['end_lineno']})\n"
        else:
            report_str += "No functions found.\n"

        return report_str

if __name__ == '__main__':
    # Example usage for demonstration purposes when the file is run directly.
    sample_code = '''
import os, sys

class MyClass:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, {self.name}!")

def my_function(a, b):
    # A simple loop
    for i in range(a):
        if i % 2 == 0:
            print(i)
    return a + b
'''
    print("--- Running Self-Analysis on Sample Code ---")
    try:
        analyzer = ASTAnalyzer(sample_code)
        analyzer.analyze()
        
        print("\n--- Formatted Report ---")
        report = analyzer.get_report()
        print(report)

        print("\n--- JSON Report ---")
        json_report = analyzer.get_report(as_json=True)
        print(json_report)

    except SyntaxError as e:
        print(f"Error parsing code: {e}")
