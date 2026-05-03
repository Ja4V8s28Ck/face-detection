from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Float, DateTime, String

from app.database import Base


class Roi(Base):
    __tablename__ = "roi"

    id = Column(Integer, primary_key=True, index=True)
    frame_index = Column(Integer, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    video_id = Column(String, nullable=False, index=True)
