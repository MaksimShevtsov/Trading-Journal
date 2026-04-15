"""Unit test: CQRS bus registration for command and query handlers."""

from __future__ import annotations

# Import handlers to trigger @command_handler / @query_handler registration
import app.application.handlers.commands.create_user_handler  # noqa: F401
import app.application.handlers.queries.get_user_handler  # noqa: F401
from app.application.bus.command_bus import CommandBus
from app.application.bus.query_bus import QueryBus
from app.application.commands.create_user import CreateUserCommand
from app.application.queries.get_user import GetUserQuery


class TestCommandBusRegistration:
    """CommandBus must discover and register command handlers (FR-006)."""

    def test_command_bus_instantiation(self):
        """CommandBus can be instantiated."""
        bus = CommandBus()
        assert bus is not None

    def test_create_user_command_registered(self):
        """CreateUserCommand handler is registered in CommandBus."""
        bus = CommandBus()
        # The handler should be discoverable for CreateUserCommand
        handler = bus._handlers.get(CreateUserCommand)
        assert handler is not None, "CreateUserCommand handler not registered"


class TestQueryBusRegistration:
    """QueryBus must discover and register query handlers (FR-006)."""

    def test_query_bus_instantiation(self):
        """QueryBus can be instantiated."""
        bus = QueryBus()
        assert bus is not None

    def test_get_user_query_registered(self):
        """GetUserQuery handler is registered in QueryBus."""
        bus = QueryBus()
        handler = bus._handlers.get(GetUserQuery)
        assert handler is not None, "GetUserQuery handler not registered"
