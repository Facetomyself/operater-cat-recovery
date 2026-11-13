from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

# Known remaining source gaps.  Keep this list small: a new entry means an
# internal import does not resolve and must be reviewed deliberately.
KNOWN_UNRESOLVED = set()

KNOWN_REDACTED_IMPORT_FILES = set()


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


def test_internal_imports_resolve_except_known_gaps():
    modules = {_module_name(path): path for path in SRC.rglob("*.py")}
    definitions = {
        name: _definitions(ast.parse(path.read_text(encoding="utf-8-sig")))
        for name, path in modules.items()
    }
    unresolved = set()
    for module, path in modules.items():
        relative = str(path.relative_to(ROOT)).replace("\\", "/")
        tree = ast.parse(path.read_text(encoding="utf-8-sig"))
        package = module if path.name == "__init__.py" else module.rsplit(".", 1)[0]
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            if node.level:
                base = package.split(".")
                if node.level > len(base):
                    continue
                prefix = ".".join(base[: len(base) - node.level + 1])
                target = f"{prefix}.{node.module}" if node.module else prefix
            else:
                target = node.module or ""
            if not target.startswith(("src.py.com.yun.mao", "src.resource")):
                continue
            if relative in KNOWN_REDACTED_IMPORT_FILES:
                continue
            if target not in modules:
                unresolved.add(
                    (
                        relative,
                        target,
                    )
                )
                continue
            for alias in node.names:
                if alias.name == "*":
                    continue
                qualified = f"{target}.{alias.name}"
                if (
                    alias.name not in definitions[target]
                    and qualified not in modules
                ):
                    unresolved.add(
                        (
                            relative,
                            qualified,
                        )
                    )
    assert unresolved <= KNOWN_UNRESOLVED
