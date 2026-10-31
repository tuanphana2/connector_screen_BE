from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Schedule


def create_schedule(db: Session, user_id: int, title: str, scheduled_at: str, platform: str = "facebook", description: str | None = None, payload: dict | None = None) -> Schedule:
    schedule = Schedule(
        user_id=user_id,
        title=title.strip(),
        description=description,
        scheduled_at=datetime.fromisoformat(scheduled_at),
        status="pending",
        platform=platform,
        payload=payload or {},
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


def list_schedules(db: Session, user_id: int | None = None) -> list[dict[str, Any]]:
    query = select(Schedule)
    if user_id is not None:
        query = query.where(Schedule.user_id == user_id)

    schedules = db.execute(query).scalars().all()
    return [
        {
            "id": item.id,
            "user_id": item.user_id,
            "title": item.title,
            "description": item.description,
            "scheduled_at": item.scheduled_at.isoformat(),
            "status": item.status,
            "platform": item.platform,
            "media_url": item.media_url,
            "payload": item.payload,
            "created_at": item.created_at.isoformat(),
        }
        for item in schedules
    ]
