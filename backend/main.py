"""FastAPI application for loan approval system."""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import router
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(
    title="Loan Approval System",
    description="Multi-Agent Agentic AI for automated loan application analysis",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Handle startup event."""
    logger.info("Loan Approval System starting up...")
    logger.info(f"Model: {settings.MODEL_NAME}")
    logger.info(f"API running on {settings.API_HOST}:{settings.API_PORT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Handle shutdown event."""
    logger.info("Loan Approval System shutting down...")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Loan Approval System API",
        "version": "1.0.0",
        "endpoints": {
            "submit_application": "/api/loan-application",
            "async_submit": "/api/loan-application/async",
            "status": "/api/loan-application/{job_id}/status",
            "health": "/api/health",
            "workflow": "/api/workflow/status",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG_MODE,
        workers=settings.API_WORKERS,
    )
