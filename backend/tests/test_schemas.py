from datetime import datetime

import pytest
from app.schemas import RoiCreate, RoiListResponse, RoiResponse, UploadResponse


class TestUploadResponse:
    def test_valid(self):
        data = UploadResponse(video_id="abc-123", total_frames=100)
        assert data.video_id == "abc-123"
        assert data.total_frames == 100

    def test_serialization(self):
        data = UploadResponse(video_id="abc-123", total_frames=50)
        result = data.model_dump()
        assert result == {"video_id": "abc-123", "total_frames": 50}


class TestRoiCreate:
    def test_valid(self):
        data = RoiCreate(
            frame_index=1,
            x=10.0,
            y=20.0,
            width=100.0,
            height=150.0,
            confidence=0.95,
            video_id="vid-1",
        )
        assert data.frame_index == 1
        assert data.confidence == 0.95

    def test_missing_fields(self):
        with pytest.raises(Exception):
            RoiCreate(frame_index=1, x=10.0)


class TestRoiResponse:
    def test_valid(self):
        data = RoiResponse(
            id=1,
            frame_index=0,
            x=50.0,
            y=60.0,
            width=200.0,
            height=250.0,
            confidence=0.9,
            timestamp=datetime(2026, 1, 1, 12, 0, 0),
            video_id="vid-1",
        )
        assert data.id == 1
        assert data.video_id == "vid-1"


class TestRoiListResponse:
    def test_valid(self):
        rois = [
            RoiResponse(
                id=1,
                frame_index=0,
                x=10.0,
                y=20.0,
                width=100.0,
                height=150.0,
                confidence=0.9,
                timestamp=datetime(2026, 1, 1),
                video_id="vid-1",
            )
        ]
        data = RoiListResponse(video_id="vid-1", total_frames=1, rois=rois)
        assert data.video_id == "vid-1"
        assert data.total_frames == 1
        assert len(data.rois) == 1
