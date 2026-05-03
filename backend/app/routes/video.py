import os
import uuid

import imageio
import numpy as np
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.detector import FaceDetector
from app.models import Roi as RoiModel
from app.schemas import RoiListResponse, RoiResponse, UploadResponse

router = APIRouter(prefix="/api", tags=["video"])

_UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(_UPLOAD_DIR, exist_ok=True)


@router.post("/video/upload", response_model=UploadResponse)
def upload_video(file: UploadFile, db: Session = Depends(get_db)):
    video_id = str(uuid.uuid4())
    file_path = os.path.join(_UPLOAD_DIR, f"{video_id}.mp4")

    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)

    reader = imageio.get_reader(file_path, "ffmpeg")
    detector = FaceDetector()

    try:
        for frame_index, frame in enumerate(reader):
            roi = detector.detect(frame)

            if roi is None:
                continue

            db_roi = RoiModel(
                frame_index=frame_index,
                x=roi.x,
                y=roi.y,
                width=roi.width,
                height=roi.height,
                confidence=roi.confidence,
                video_id=video_id,
            )
            db.add(db_roi)

        db.commit()
    finally:
        detector.close()
        reader.close()

    return UploadResponse(video_id=video_id, total_frames=frame_index + 1)


@router.get("/roi/{video_id}", response_model=RoiListResponse)
def get_roi(video_id: str, db: Session = Depends(get_db)):
    rois = (
        db.query(RoiModel)
        .filter(RoiModel.video_id == video_id)
        .order_by(RoiModel.frame_index)
        .all()
    )

    if not rois:
        raise HTTPException(
            status_code=404, detail=f"No ROI data for video {video_id}")

    return RoiListResponse(
        video_id=video_id,
        total_frames=len(rois),
        rois=[RoiResponse.model_validate(r) for r in rois],
    )
