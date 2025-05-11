from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

from app.core.config import settings
from app.routers import auth, user, employee, department, onboarding

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

print(f"Connected to database: {settings.DATABASE_URL}")

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(user.router, prefix=settings.API_V1_STR)
app.include_router(employee.router, prefix=settings.API_V1_STR)
app.include_router(department.router, prefix=settings.API_V1_STR)
app.include_router(onboarding.router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    """
    Actions to run on application startup.
    """
    logger.info("Starting up FlowWork HR Automation API")
    
    # Create uploads directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    logger.info(f"Ensuring upload directory exists: {settings.UPLOAD_DIR}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions to run on application shutdown.
    """
    logger.info("Shutting down FlowWork HR Automation API")


@app.get("/")
async def root():
    """
    Root endpoint for health check.
    """
    return {
        "status": "online",
        "name": settings.PROJECT_NAME,
        "api_version": settings.API_V1_STR,
    }