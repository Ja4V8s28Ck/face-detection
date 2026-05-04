import pytest
import numpy as np
from app.detector import FaceDetector, Roi


@pytest.fixture
def detector():
    det = FaceDetector()
    yield det
    det.close()


@pytest.fixture
def blank_frame():
    return np.zeros((480, 640, 3), dtype=np.uint8)


class TestFaceDetector:
    def test_detect_no_face(self, detector, blank_frame):
        result = detector.detect(blank_frame)
        assert result is None

    def test_detect_returns_roi_or_none(self, detector, blank_frame):
        result = detector.detect(blank_frame)
        assert result is None or isinstance(result, Roi)

    def test_draw_roi_returns_numpy_array(self, detector, blank_frame):
        roi = Roi(x=100, y=50, width=200, height=250, confidence=0.95)
        drawn = detector.draw_roi(blank_frame, roi)
        assert isinstance(drawn, np.ndarray)

    def test_draw_roi_preserves_dimensions(self, detector, blank_frame):
        roi = Roi(x=100, y=50, width=200, height=250, confidence=0.95)
        drawn = detector.draw_roi(blank_frame, roi)
        assert drawn.shape == blank_frame.shape

    def test_draw_roi_modifies_pixels(self, detector, blank_frame):
        roi = Roi(x=100, y=50, width=200, height=250, confidence=0.95)
        drawn = detector.draw_roi(blank_frame, roi)
        assert not np.array_equal(drawn, blank_frame)

    def test_draw_roi_red_pixels_present(self, detector, blank_frame):
        roi = Roi(x=100, y=50, width=200, height=250, confidence=0.95)
        drawn = detector.draw_roi(blank_frame, roi)
        red_pixels = np.any(drawn[:, :, 0] > 0)
        assert red_pixels

    def test_roi_bounds_respected(self, detector, blank_frame):
        roi = Roi(x=-10, y=-10, width=9999, height=9999, confidence=0.95)
        drawn = detector.draw_roi(blank_frame, roi)
        assert drawn.shape == blank_frame.shape
