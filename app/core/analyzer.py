import ast
from pathlib import Path
from typing import List, Set


class FunctionAnalyzer(ast.NodeVisitor):
    """
    Analyzes Python source code to extract:
    - Function definitions
    - Function calls
    """

    def __init__(self):
        self.defined_functions: Set[str] = set()
        self.called_functions: Set[str] = set()

    def visit_FunctionDef(self, node):
        self.defined_functions.add(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.called_functions.add(node.func.id)
        self.generic_visit(node)


class CodeAnalyzer:
    """
    Main analyzer class to detect unused functions
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def analyze(self) -> dict:
        source_code = self.file_path.read_text(encoding="utf-8")
        tree = ast.parse(source_code)

        analyzer = FunctionAnalyzer()
        analyzer.visit(tree)

        unused_functions = analyzer.defined_functions - analyzer.called_functions
        return {
            "defined": analyzer.defined_functions,
            "called": analyzer.called_functions,
            "unused": unused_functions
        }