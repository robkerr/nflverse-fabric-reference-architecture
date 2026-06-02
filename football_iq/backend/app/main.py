"""Football IQ — FastAPI backend entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import situation

app = FastAPI(
    title="Football IQ API",
    description="NFL analytics API powered by Microsoft Fabric data lake.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(situation.router)


@app.get("/health")
def health():
    return {"status": "ok"}
