import ast
import builtins
from pathlib import Path
from platform import node
from typing import Set


class FunctionAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.defined_functions: Set[str] = set()
        self.called_functions: Set[str] = set()

    def visit_FunctionDef(self, node):
        self.defined_functions.add(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        # Direct function call: func()
        if isinstance(node.func, ast.Name):
            self.called_functions.add(node.func.id)
        # Attribute call: obj.func()
        elif isinstance(node.func, ast.Attribute):
            self.called_functions.add(node.func.attr)
        self.generic_visit(node)


class CodeAnalyzer:

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

    def analyze_project(self) -> dict:
        defined_all = set()
        called_all = set()

        for file in self.file_path.rglob("*.py"):
            source_code = file.read_text(encoding="utf-8")
            tree = ast.parse(source_code)

            analyzer = FunctionAnalyzer()
            analyzer.visit(tree)

            defined_all.update(analyzer.defined_functions)
            called_all.update(analyzer.called_functions)

        # Ignore built-in functions like print, len, etc.
        builtins_set = set(dir(builtins))
        filtered_called = {func for func in called_all if func not in builtins_set}

        unused = defined_all - filtered_called

        return {
            "defined": defined_all,
            "called": filtered_called,
            "unused": unused
        }