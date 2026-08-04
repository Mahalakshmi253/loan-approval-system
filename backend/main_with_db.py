"""FastAPI application with MySQL database integration."""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.database import create_all_tables, get_db
from backend.routes.loan_routes_with_db import router
from config import settings
from utils.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app startup and shutdown events."""
    # Startup
    logger.info("🚀 Application starting up...")
    logger.info(f"📊 Model: {settings.MODEL_NAME}")
    logger.info(f"🌐 API running on {settings.API_HOST}:{settings.API_PORT}")
    logger.info("🗄️  Creating database tables...")
    try:
        create_all_tables()
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create database tables: {str(e)}")

    yield

    # Shutdown
    logger.info("🛑 Application shutting down...")


app = FastAPI(
    title="Loan Approval System",
    description="Multi-Agent Agentic AI for automated loan application analysis with MySQL",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "🏦 Loan Approval System API",
        "version": "2.0.0",
        "database": "MySQL Connected",
        "endpoints": {
            "submit_application": "POST /api/loan-application",
            "get_application": "GET /api/applications/{applicant_id}",
            "get_all_applications": "GET /api/applications",
            "get_decision": "GET /api/applications/{applicant_id}/decision",
            "statistics": "GET /api/statistics",
            "health": "GET /api/health",
            "docs": "/docs"
        },
    }


@app.get("/database/status")
async def database_status():
    """Check database connection status."""
    try:
        db_session = next(get_db())
        db_session.execute("SELECT 1")
        db_session.close()
        return {
            "status": "connected",
            "message": "✅ MySQL database is connected",
            "database": "loan_approval_system"
        }
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return {
            "status": "disconnected",
            "message": f"❌ MySQL connection failed: {str(e)}",
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main_with_db:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG_MODE,
        workers=settings.API_WORKERS,
    )
