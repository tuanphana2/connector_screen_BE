from .analytics import router as analytics_router
from .auth import router as auth_router
from .dashboard import router as dashboard_router
from .platforms import router as platforms_router
from .publishing import router as publishing_router
from .schedule import router as schedule_router
from .videos import router as videos_router

__all__ = [
    "auth_router",
    "dashboard_router",
    "videos_router",
    "schedule_router",
    "analytics_router",
    "platforms_router",
    "publishing_router",
]
