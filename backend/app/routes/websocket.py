import base64
import io
import os

import imageio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from PIL import Image as PILImage

from app.detector import FaceDetector

router = APIRouter(prefix="/ws", tags=["websocket"])

_UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")


@router.websocket("/video/{video_id}")
async def stream_video(websocket: WebSocket, video_id: str):
    await websocket.accept()

    file_path = os.path.join(_UPLOAD_DIR, f"{video_id}.mp4")
    if not os.path.exists(file_path):
        await websocket.send_json({"error": f"Video {video_id} not found"})
        await websocket.close()
        return

    detector = FaceDetector()
    reader = imageio.get_reader(file_path, "ffmpeg")

    try:
        for frame_index, frame in enumerate(reader):
            roi = detector.detect(frame)

            if roi:
                pil_image = detector.draw_roi(frame, roi)
            else:
                pil_image = PILImage.fromarray(frame)

            buf = io.BytesIO()
            pil_image.save(buf, format="JPEG", quality=85)
            buf.seek(0)
            frame_base64 = base64.b64encode(buf.read()).decode("utf-8")

            message = {
                "frame_index": frame_index,
                "frame": frame_base64,
                "roi": (
                    {
                        "x": roi.x,
                        "y": roi.y,
                        "width": roi.width,
                        "height": roi.height,
                        "confidence": roi.confidence,
                    }
                    if roi
                    else None
                ),
            }

            await websocket.send_json(message)
    except WebSocketDisconnect:
        pass
    finally:
        detector.close()
        reader.close()
