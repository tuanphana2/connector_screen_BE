from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Account, User


def create_user_profile(db: Session, full_name: str, email: str, phone: str | None = None) -> User:
    email = email.strip().lower()
    user = db.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if user is None:
        user = User(full_name=full_name.strip(), email=email, phone=phone, is_active=True)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def create_account(db: Session, user_id: int, email: str, password_hash: str | None = None, provider: str = "local") -> Account:
    account = db.execute(
        select(Account).where(Account.provider == provider, Account.email == email.strip().lower())
    ).scalar_one_or_none()
    if account is None:
        account = Account(user_id=user_id, provider=provider, email=email.strip().lower(), password_hash=password_hash, is_active=True)
        db.add(account)
        db.commit()
        db.refresh(account)
    return account


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.execute(select(User).where(User.email == email.strip().lower())).scalar_one_or_none()


def get_account_by_email(db: Session, email: str, provider: str = "local") -> Account | None:
    return db.execute(
        select(Account).where(Account.provider == provider, Account.email == email.strip().lower())
    ).scalar_one_or_none()


def list_users(db: Session) -> list[dict[str, Any]]:
    users = db.execute(select(User)).scalars().all()
    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "avatar_url": user.avatar_url,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat(),
        }
        for user in users
    ]
