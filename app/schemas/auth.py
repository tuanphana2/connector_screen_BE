from __future__ import annotations

from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str | None = None
    password: str | None = None


class GoogleLoginRequest(BaseModel):
    email: str | None = None
    name: str | None = None


class ForgotPasswordRequest(BaseModel):
    email: str | None = None
