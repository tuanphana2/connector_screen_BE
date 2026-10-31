from __future__ import annotations

from fastapi import APIRouter

from app.state import state

router = APIRouter(tags=["analytics"])


@router.get("/api/analytics")
def analytics() -> dict:
    return {"data": state["analytics"]}
