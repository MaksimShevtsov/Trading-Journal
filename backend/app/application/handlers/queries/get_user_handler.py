"""GetUserQuery handler."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from app.application.bus.query_bus import query_handler
from app.application.queries.get_user import GetUserQuery
from app.domain.errors import NotFoundError
from app.infrastructure.db.queries.user_queries import fetch_user_by_id

if TYPE_CHECKING:
    from app.application.read_models.user_read_model import UserReadModel


@query_handler(GetUserQuery)
async def handle_get_user(query: GetUserQuery, *, engine: Any) -> UserReadModel:
    """Handle user retrieval: fetch from SQL, return read model."""
    result = await fetch_user_by_id(engine, query.user_id)
    if result is None:
        raise NotFoundError(code="USER_NOT_FOUND", message="User not found")
    return result
