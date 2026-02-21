import ast
import builtins
from pathlib import Path
from typing import Set


class FunctionAnalyzer(ast.NodeVisitor):

    def __init__(self):
        # Store function metadata
        self.defined_functions = {}
        self.called_functions: Set[str] = set()

    def visit_FunctionDef(self, node):
        self.defined_functions[node.name] = {
            "line": node.lineno
        }
        self.generic_visit(node)

    def visit_Call(self, node):
        # Direct call: func()
        if isinstance(node.func, ast.Name):
            self.called_functions.add(node.func.id)

        # Attribute call: obj.func()
        elif isinstance(node.func, ast.Attribute):
            self.called_functions.add(node.func.attr)

        self.generic_visit(node)


class CodeAnalyzer:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def analyze_project(self) -> dict:
        defined_all = {}
        called_all = set()

        for file in self.file_path.rglob("*.py"):
            source_code = file.read_text(encoding="utf-8")
            tree = ast.parse(source_code)

            analyzer = FunctionAnalyzer()
            analyzer.visit(tree)

            # Store function name + file + line
            for func_name, metadata in analyzer.defined_functions.items():
                defined_all[func_name] = {
                    "file": str(file),
                    "line": metadata["line"]
                }

            called_all.update(analyzer.called_functions)

        # Remove built-in functions
        builtins_set = set(dir(builtins))
        filtered_called = {func for func in called_all if func not in builtins_set}

        # Detect unused functions
        unused = {
            name: info
            for name, info in defined_all.items()
            if name not in filtered_called
        }

        return {
            "defined": defined_all,
            "called": filtered_called,
            "unused": unused
        }