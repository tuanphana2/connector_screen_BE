from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.content import GenerateVideoRequest
from app.state import state

router = APIRouter(tags=["videos"])


@router.post("/api/videos/generate")
def generate_video(payload: GenerateVideoRequest) -> dict:
    prompt = (payload.prompt or "").strip()
    selected_videos = payload.selectedVideos or []
    local_files = payload.localFiles or []

    if not prompt and not selected_videos and not local_files:
        raise HTTPException(status_code=400, detail={"message": "Hãy nhập yêu cầu hoặc chọn video trước nhé!"})

    new_video = {
        "id": __import__("time").time_ns() // 1_000_000,
        "duration": "00:00",
        "source": "Từ máy",
        "category": "Video AI",
        "title": prompt or "Video mới từ thư viện",
        "description": "Vừa tạo",
        "views": "0",
        "status": "processing",
        "platforms": ["facebook", "youtube"],
    }

    state["videos"].insert(0, new_video)
    return {"message": "Yêu cầu dựng video đã được gửi cho AI.", "video": new_video}
