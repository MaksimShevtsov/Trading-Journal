"""Integration test: SQLRegistry loads .sql files and resolves dot-keys."""

from __future__ import annotations

from pathlib import Path

import pytest
from row_query import SQLRegistry

SQL_ROOT = Path(__file__).parent.parent.parent / "app" / "infrastructure" / "sql"


class TestSQLRegistry:
    """SQLRegistry must load and resolve SQL files via dot-keys (FR-007)."""

    @pytest.fixture
    def registry(self):
        """Create a SQLRegistry pointing at the app SQL directory."""
        return SQLRegistry(root_dir=str(SQL_ROOT))

    def test_registry_instantiation(self, registry):
        """SQLRegistry can be instantiated with the app SQL directory."""
        assert registry is not None

    def test_users_insert_resolves(self, registry):
        """users.insert key resolves to a SQL file."""
        sql = registry.get("users.insert")
        assert sql is not None
        assert "INSERT INTO users" in sql

    def test_users_get_by_id_resolves(self, registry):
        """users.get_by_id key resolves to a SQL file."""
        sql = registry.get("users.get_by_id")
        assert sql is not None
        assert "SELECT" in sql
        assert ":id" in sql

    def test_users_get_by_email_resolves(self, registry):
        """users.get_by_email key resolves to a SQL file."""
        sql = registry.get("users.get_by_email")
        assert sql is not None
        assert "SELECT" in sql
        assert ":email" in sql

    def test_users_list_all_resolves(self, registry):
        """users.list_all key resolves to a SQL file."""
        sql = registry.get("users.list_all")
        assert sql is not None
        assert "SELECT" in sql

    def test_no_password_hash_in_insert(self, registry):
        """users.insert must NOT contain password_hash column."""
        sql = registry.get("users.insert")
        assert "password_hash" not in sql

    def test_no_password_hash_in_selects(self, registry):
        """No SQL file should reference password_hash column."""
        for key in ["users.get_by_id", "users.get_by_email", "users.list_all"]:
            sql = registry.get(key)
            assert "password_hash" not in sql, f"{key} references password_hash"

    def test_parameter_syntax(self, registry):
        """SQL files use :name parameter syntax."""
        sql = registry.get("users.insert")
        assert ":id" in sql
        assert ":name" in sql
        assert ":email" in sql
