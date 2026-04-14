"""Contract tests for error envelope format."""

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


class TestErrorEnvelope:
    """Contract tests for the standardized error envelope."""

    def test_validation_error_envelope(self, client):
        """Pydantic validation errors return the error envelope format."""
        response = client.post(
            "/api/v1/users",
            json={},  # Missing required fields
        )
        assert response.status_code == 422
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "VALIDATION_ERROR"
        assert data["error"]["message"] == "Request validation failed"
        assert isinstance(data["error"]["details"], dict)
