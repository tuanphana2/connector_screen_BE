from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./connector_screen.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    from app.models import Account, IntegrationConfig, Schedule, User  # noqa: F401

    Base.metadata.create_all(bind=engine)
    seed_demo_data()


def seed_demo_data() -> None:
    from app.services.auth_service import hash_password
    from app.models import Account, IntegrationConfig, User

    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            user = User(full_name="Nhu Admin", email="abc@gmail.com", phone="0900000000", is_active=True)
            db.add(user)
            db.commit()
            db.refresh(user)

            db.add(
                Account(
                    user_id=user.id,
                    provider="local",
                    email="abc@gmail.com",
                    password_hash=hash_password("123456"),
                    is_active=True,
                )
            )
            db.add(
                IntegrationConfig(
                    user_id=user.id,
                    provider="goclaw",
                    name="Goclaw Demo",
                    api_key="demo_goclaw_key",
                    api_secret="demo_goclaw_secret",
                    base_url="https://api.goclaw.com",
                    project_id="demo-project",
                    config_json={"workspace": "demo"},
                    is_active=True,
                )
            )
            db.add(
                IntegrationConfig(
                    user_id=user.id,
                    provider="cloudinary",
                    name="Cloudinary Demo",
                    api_key="demo_cloudinary_key",
                    api_secret="demo_cloudinary_secret",
                    base_url="https://res.cloudinary.com",
                    project_id="demo-project",
                    config_json={"cloud_name": "demo-cloud"},
                    is_active=True,
                )
            )
            db.commit()
    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
