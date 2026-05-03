from fastapi import FastAPI

app = FastAPI(
    title="Real-Time Face Detection Video Streaming System",
    description="Video face detection with ROI bounding boxes",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}
