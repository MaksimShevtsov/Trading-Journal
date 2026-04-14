"""Unit test: domain layer must have zero framework imports."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

# Packages that must NOT appear in domain layer imports
FORBIDDEN_IMPORTS = {"fastapi", "pydantic", "row_query", "sqlalchemy", "psycopg"}

DOMAIN_ROOT = Path(__file__).parent.parent.parent / "app" / "domain"


def _collect_python_files(root: Path) -> list[Path]:
    """Recursively collect all .py files under the domain root."""
    return sorted(root.rglob("*.py"))


def _extract_import_names(file_path: Path) -> set[str]:
    """Parse a Python file and extract all top-level imported package names."""
    source = file_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(file_path))

    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])

    return names


class TestDomainPurity:
    """Domain layer must never import from frameworks (FR-005, SC-004)."""

    @pytest.mark.parametrize(
        "file_path",
        _collect_python_files(DOMAIN_ROOT),
        ids=lambda p: str(p.relative_to(DOMAIN_ROOT)),
    )
    def test_no_framework_imports(self, file_path: Path):
        """Each domain file must have zero forbidden framework imports."""
        import_names = _extract_import_names(file_path)
        violations = import_names & FORBIDDEN_IMPORTS
        assert not violations, f"{file_path.relative_to(DOMAIN_ROOT)} imports forbidden packages: {violations}"

    def test_domain_root_exists(self):
        """Domain directory must exist."""
        assert DOMAIN_ROOT.is_dir()

    def test_domain_has_files(self):
        """Domain directory must contain Python files."""
        py_files = _collect_python_files(DOMAIN_ROOT)
        assert len(py_files) > 0, "Domain directory is empty"
