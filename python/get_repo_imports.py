import ast
import subprocess
import pprint
import sys

def scan_for_imports() -> None:
    git_files: list[str] = subprocess.check_output(
        ["git", "ls-files"],
    ).decode("ascii").split("\n")

    py_files = [i for i in git_files if i[-3:] == ".py"]

    imports = set() 
    for file in py_files:
        with open(file, "r") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module_name = node.module
                for alias in node.names:
                    imports.add(f"{module_name}.{alias.name}")

    imports = [i for i in imports if i not in list(sys.modules.keys())]
    pprint.pprint(sorted(imports))

    # with open("setup.py", "r") as f:
    #     tree = ast.parse(f.read())
    #
    # for node in ast.walk(tree):
    #     if isinstance(node, ast.Assign):
    #         for target in node.targets:
    #             if isinstance(target, ast.Name) and target.id == 'install_requires':
    #                 if isinstance(node.value, ast.List):
    #                     node.value.elts.append(imports)
    #                     node.value.elts.sort()

    # Write to setup.py here


scan_for_imports()
