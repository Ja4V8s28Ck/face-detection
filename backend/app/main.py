from fastapi import FastAPI

from app.database import engine, Base
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Real-Time Face Detection Video Streaming System",
    description="Video face detection with ROI bounding boxes",
    version="1.0.0",
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
