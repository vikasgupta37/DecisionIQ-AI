from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1 import auth, dashboard, upload, processing
from backend.app.core.config import settings
from backend.app.core.database import Base, engine
from backend.app.core.exceptions import setup_exception_handlers

# Import models to ensure they are registered with SQLAlchemy Base for auto-creation
from backend.app.models.user import User
from backend.app.models.dataset import Dataset
from backend.app.models.insight import AIInsight
from backend.app.models.activity import ActivityLog
from backend.app.models.processing_report import ProcessingReport


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI Lifespan events.
    At startup: verifies and creates database tables for local running.
    At shutdown: clean up connections if needed.
    """
    # Create tables automatically at startup (helpful for development/tests)
    if settings.SQLALCHEMY_DATABASE_URI and settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set up CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Setup custom exceptions handlers
setup_exception_handlers(app)

# Include routes
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["Dashboard"])
app.include_router(upload.router, prefix=f"{settings.API_V1_STR}/upload", tags=["File Upload"])
app.include_router(processing.router, prefix=f"{settings.API_V1_STR}/processing", tags=["Data Processing"])


@app.get("/")
def read_root():
    """DecisionIQ AI API Root Endpoint"""
    return {
        "platform": settings.PROJECT_NAME,
        "version": "1.0.0",
        "docs_url": "/docs",
        "status": "healthy"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
