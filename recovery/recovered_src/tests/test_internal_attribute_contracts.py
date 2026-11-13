from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def _module_name(path: Path) -> str:
    relative = path.relative_to(ROOT)
    parts = list(relative.parts)
    if parts[-1] == "__init__.py":
        return ".".join(parts[:-1])
    return ".".join(parts[:-1] + [path.stem])


def _definitions(tree: ast.Module) -> set[str]:
    names = {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }
    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        else:
            targets = []
        for target in targets:
            if isinstance(target, ast.Name):
                names.add(target.id)
        if isinstance(node, ast.ImportFrom):
            names.update(alias.asname or alias.name for alias in node.names)
        elif isinstance(node, ast.Import):
            names.update(
                alias.asname or alias.name.split(".", 1)[0]
                for alias in node.names
            )
    return names


def test_internal_module_attributes_resolve():
    modules = {_module_name(path): path for path in SRC.rglob("*.py")}
    definitions = {
        name: _definitions(ast.parse(path.read_text(encoding="utf-8-sig")))
        for name, path in modules.items()
    }
    missing = set()
    for module, path in modules.items():
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        aliases: dict[str, str] = {}
        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    full = alias.name
                    local = alias.asname or full.split(".", 1)[0]
                    if full in modules:
                        aliases[local] = full
                    elif local in modules:
                        aliases[local] = local
            elif isinstance(node, ast.ImportFrom):
                base = node.module or ""
                if node.level:
                    package = (
                        module
                        if path.name == "__init__.py"
                        else module.rsplit(".", 1)[0]
                    )
                    parts = package.split(".")
                    if node.level <= len(parts):
                        prefix = ".".join(parts[: len(parts) - node.level + 1])
                        base = f"{prefix}.{base}" if base else prefix
                for alias in node.names:
                    full = f"{base}.{alias.name}" if base else alias.name
                    if full in modules:
                        aliases[alias.asname or alias.name] = full
        for node in ast.walk(tree):
            if not isinstance(node, ast.Attribute):
                continue
            if not isinstance(node.value, ast.Name):
                continue
            target = aliases.get(node.value.id)
            if target is None:
                continue
            if node.attr not in definitions[target]:
                missing.add(
                    (
                        str(path.relative_to(ROOT)).replace("\\", "/"),
                        node.lineno,
                        target,
                        node.attr,
                    )
                )
    assert missing == set()
