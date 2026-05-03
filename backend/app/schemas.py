from datetime import datetime

from pydantic import BaseModel


class UploadResponse(BaseModel):
    video_id: str
    total_frames: int


class RoiCreate(BaseModel):
    frame_index: int
    x: float
    y: float
    width: float
    height: float
    confidence: float
    video_id: str


class RoiResponse(BaseModel):
    id: int
    frame_index: int
    x: float
    y: float
    width: float
    height: float
    confidence: float
    timestamp: datetime
    video_id: str

    model_config = {"from_attributes": True}


class RoiListResponse(BaseModel):
    video_id: str
    total_frames: int
    rois: list[RoiResponse]
