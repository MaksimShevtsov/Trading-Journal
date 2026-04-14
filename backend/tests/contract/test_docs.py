"""Contract tests for API documentation endpoint."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.infrastructure.config import Settings
from app.main import create_app


@pytest.fixture
def client():
    """Create a test client with mock app state (no database needed)."""
    app = create_app()
    app.state.settings = Settings()
    mock_engine = MagicMock()
    mock_engine.close = AsyncMock()
    app.state.engine = mock_engine
    return TestClient(app, raise_server_exceptions=True)


class TestDocsEndpoint:
    """Contract tests for GET /docs (Swagger UI)."""

    def test_docs_returns_200(self, client):
        """API documentation endpoint returns 200 status."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_docs_returns_html(self, client):
        """API documentation returns HTML content."""
        response = client.get("/docs")
        assert "text/html" in response.headers.get("content-type", "")

    def test_openapi_schema_accessible(self, client):
        """OpenAPI schema is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "paths" in schema

    def test_registered_endpoints_in_schema(self, client):
        """Registered endpoints appear in the OpenAPI schema."""
        response = client.get("/openapi.json")
        schema = response.json()
        paths = schema.get("paths", {})
        assert "/health" in paths
        assert "/api/v1/users" in paths
