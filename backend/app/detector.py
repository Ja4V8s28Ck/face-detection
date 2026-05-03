import os
from dataclasses import dataclass

import numpy as np
from mediapipe import Image as MpImage, ImageFormat
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import FaceDetector as MpFaceDetector
from mediapipe.tasks.python.vision import FaceDetectorOptions, RunningMode
from PIL import Image as PILImage, ImageDraw

_MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "blaze_face_short_range.tflite")


@dataclass
class Roi:
    x: int
    y: int
    width: int
    height: int
    confidence: float


class FaceDetector:
    def __init__(self):
        base_options = BaseOptions(model_asset_path=_MODEL_PATH)
        options = FaceDetectorOptions(
            base_options=base_options,
            running_mode=RunningMode.IMAGE,
            min_detection_confidence=0.5,
        )
        self._detector = MpFaceDetector.create_from_options(options)

    def close(self):
        self._detector.close()

    def detect(self, frame: np.ndarray) -> Roi | None:
        h, w = frame.shape[:2]
        mp_image = MpImage(image_format=ImageFormat.SRGB, data=frame)
        result = self._detector.detect(mp_image)

        if not result.detections:
            return None

        detection = result.detections[0]
        bbox = detection.bounding_box
        score = detection.categories[0].score

        return Roi(
            x=max(0, bbox.origin_x),
            y=max(0, bbox.origin_y),
            width=min(bbox.width, w - bbox.origin_x),
            height=min(bbox.height, h - bbox.origin_y),
            confidence=score,
        )

    def draw_roi(self, image: np.ndarray, roi: Roi) -> PILImage.Image:
        pil_image = PILImage.fromarray(image)
        draw = ImageDraw.Draw(pil_image)
        draw.rectangle(
            [(roi.x, roi.y), (roi.x + roi.width, roi.y + roi.height)],
            outline="red",
            width=3,
        )
        return pil_image
