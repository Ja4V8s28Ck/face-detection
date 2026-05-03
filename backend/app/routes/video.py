import os
import uuid

import imageio
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.detector import CONFIDENCE_THRESHOLD, DETECT_EVERY_N_FRAMES, FaceDetector, Roi
from app.models import Roi as RoiModel
from app.schemas import RoiListResponse, RoiResponse, UploadResponse

router = APIRouter(prefix="/api", tags=["video"])

_UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(_UPLOAD_DIR, exist_ok=True)


@router.post("/video/upload", response_model=UploadResponse)
def upload_video(file: UploadFile, db: Session = Depends(get_db)):
    video_id = str(uuid.uuid4())
    input_path = os.path.join(_UPLOAD_DIR, f"{video_id}.mp4")
    output_path = os.path.join(_UPLOAD_DIR, f"processed_{video_id}.mp4")

    with open(input_path, "wb") as f:
        f.write(file.file.read())

    reader = imageio.get_reader(input_path, "ffmpeg")
    meta = reader.get_meta_data()
    fps = meta.get("fps", 30)
    frame_size = meta.get("size")

    if not frame_size:
        raise HTTPException(
            status_code=400, detail="Could not read video metadata")

    writer = imageio.get_writer(
        output_path, fps=fps, codec="libx264", macro_block_size=1)
    detector = FaceDetector()
    last_roi: Roi | None = None
    total_frames = 0

    try:
        for frame in reader:
            total_frames += 1

            should_detect = total_frames == 1 or (
                total_frames - 1) % DETECT_EVERY_N_FRAMES == 0

            if should_detect:
                roi = detector.detect(frame)
                if roi and roi.confidence >= CONFIDENCE_THRESHOLD:
                    last_roi = roi
                elif roi is None:
                    last_roi = None

            if last_roi:
                frame = detector.draw_roi(frame, last_roi)
                writer.append_data(frame)

                db_roi = RoiModel(
                    frame_index=total_frames - 1,
                    x=last_roi.x,
                    y=last_roi.y,
                    width=last_roi.width,
                    height=last_roi.height,
                    confidence=last_roi.confidence,
                    video_id=video_id,
                )
                db.add(db_roi)
            else:
                writer.append_data(frame)

        db.commit()
    finally:
        reader.close()
        writer.close()
        detector.close()
        if os.path.exists(input_path):
            os.remove(input_path)

    if total_frames == 0:
        raise HTTPException(status_code=400, detail="Video has no frames")

    return UploadResponse(video_id=video_id, total_frames=total_frames)


@router.get("/video/{video_id}/stream")
def stream_video(video_id: str):
    file_path = os.path.join(_UPLOAD_DIR, f"processed_{video_id}.mp4")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Processed video {
                            video_id} not found")

    return FileResponse(
        file_path,
        media_type="video/mp4",
        filename=f"processed_{video_id}.mp4",
    )


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
