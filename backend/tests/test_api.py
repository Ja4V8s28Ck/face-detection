import tempfile
from pathlib import Path

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.routes.video import router as video_router


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test.db")


@pytest.fixture
def engine(db_path):
    return create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})


@pytest.fixture
def session(engine):
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def override_get_db(session):
    def _get():
        yield session

    return _get


@pytest.fixture
def client(session, engine):
    def get_test_db():
        yield session

    app = FastAPI()
    app.include_router(video_router)
    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as c:
        yield c


class TestRoiEndpoint:
    def test_get_roi_not_found(self, client):
        response = client.get("/api/roi/nonexistent-id")
        assert response.status_code == 404
        assert "nonexistent-id" in response.json()["detail"]


class TestVideoStream:
    def test_stream_video_not_found(self, client):
        response = client.get("/api/video/nonexistent-id/stream")
        assert response.status_code == 404
        assert "nonexistent-id" in response.json()["detail"]
