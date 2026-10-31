from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    analytics_router,
    auth_router,
    dashboard_router,
    platforms_router,
    publishing_router,
    schedule_router,
    videos_router,
)
from app.config import APP_TITLE, APP_VERSION
from app.database import init_db

app = FastAPI(title=APP_TITLE, version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(videos_router)
app.include_router(schedule_router)
app.include_router(analytics_router)
app.include_router(platforms_router)
app.include_router(publishing_router)


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "message": "Backend đang chạy"}
