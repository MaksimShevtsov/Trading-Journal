"""User request/response schemas."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):
    """Request schema for creating a user."""

    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class UserResponse(BaseModel):
    """Response schema for user data."""

    id: str
    name: str
    email: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
