"""Contract tests for the health endpoint."""

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
    # Mock engine to avoid database connection
    mock_engine = MagicMock()
    mock_engine.close = AsyncMock()
    app.state.engine = mock_engine
    return TestClient(app, raise_server_exceptions=True)


class TestHealthEndpoint:
    """Contract tests for GET /health."""

    def test_health_returns_200(self, client):
        """Health endpoint returns 200 status."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_healthy_status(self, client):
        """Health endpoint returns 'healthy' status."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"

    def test_health_returns_service_name(self, client):
        """Health endpoint returns configured service name."""
        response = client.get("/health")
        data = response.json()
        assert data["service"] == "Trading Journal"

    def test_health_response_matches_contract(self, client):
        """Full response matches the health-api.md contract."""
        response = client.get("/health")
        data = response.json()
        assert set(data.keys()) == {"status", "service"}
        assert data["status"] == "healthy"
        assert isinstance(data["service"], str)
