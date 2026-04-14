"""Flow compositions for request pipeline."""

from __future__ import annotations

from fastapi_request_pipeline import AllowAnonymous, Flow

from app.interfaces.pipeline.stages.auth import AuthenticationStage
from app.interfaces.pipeline.stages.logging_stage import LoggingStage
from app.interfaces.pipeline.stages.permission import PermissionStage

# Public routes (health, webhooks) — no auth, no rate limiting
public_flow = Flow(
    AllowAnonymous(),
    LoggingStage(),
)

# Authenticated user flow — stub auth for now, Clerk integration in future story
authenticated_flow = Flow(
    AuthenticationStage(),
    PermissionStage(),
    LoggingStage(),
)
