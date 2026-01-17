"""
Wevolve API - Main Entry Point
The AI-Powered Career Acceleration Ecosystem

Three Core Modules:
1. Resume Intelligence - Parse and score resumes
2. Transparent Matching - Multi-factor job matching with explanations
3. Actionable Growth - Personalized learning roadmaps
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import init_db
from .schemas import HealthResponse
from .routers import resume, matching, roadmap

# ============================================================
# Application Setup
# ============================================================

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(resume.router)
app.include_router(matching.router)
app.include_router(roadmap.router)


# ============================================================
# Lifecycle Events
# ============================================================

@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup."""
    print("🚀 Wevolve API Starting...")
    init_db()
    print("✅ Database initialized successfully!")


# ============================================================
# Health Check Endpoints
# ============================================================

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check."""
    return HealthResponse(
        status="healthy",
        message="Welcome to Wevolve API - The AI-Powered Career Acceleration Ecosystem",
        version=settings.APP_VERSION
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check."""
    return HealthResponse(
        status="healthy",
        message="All systems operational",
        version=settings.APP_VERSION
    )


# ============================================================
# Run with: uvicorn app.main:app --reload
# ============================================================
