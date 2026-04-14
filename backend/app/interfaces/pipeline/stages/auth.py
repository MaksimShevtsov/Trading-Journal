"""Authentication pipeline stage — Clerk JWT verification stub.

This is a pass-through stub. Clerk integration will be implemented in a future story.
"""

from __future__ import annotations

from fastapi_request_pipeline import ComponentCategory, FlowComponent, RequestContext


class AuthenticationStage(FlowComponent):
    """Stub authentication stage for development.

    Passes through all requests without authentication.
    Clerk JWT verification will be added in a future story.
    """

    category = ComponentCategory.AUTHENTICATION

    async def resolve(self, ctx: RequestContext) -> None:
        """Pass through without authentication check."""
        ctx.state["authenticated"] = True
