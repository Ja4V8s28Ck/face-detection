from fastapi import APIRouter

from app.routes.video import router as video_router

router = APIRouter()
router.include_router(video_router)
