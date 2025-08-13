"""
SkillMatch Backend API
A FastAPI application for tracking developer skills, projects,
and generating AI-powered portfolio suggestions.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import time

from app.core.config import settings
from app.core.exceptions import SkillMatchException
from app.core.middleware import register_middlewares

from app.models import *
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting SkillMatch Backend API")
    yield


app = FastAPI(lifespan=lifespan)


#
register_middlewares(app)


# Exception Handler
@app.exception_handler(SkillMatchException)
async def skillmatch_exception_handler(request: Request, exc: SkillMatchException):
    """
    handle skill match exceptions
    """
    return JSONResponse(
        status_code= exc.status_code,
        content={
            "error": True,
            "message": exc.message,
            "type": exc.__class__.__name__,
            "path": request.url.path,
            "timestamp": time.time()

        }
    )


#Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    handle global exceptions
    """
    message = "Internal Server Error" if settings.ENVIRONMENT == "production" else str(exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": message,
            "type": "InternalServerError",
            "path": request.url.path,
            "timestamp": time.time()
        }
    )


@app.get("/")
async def root():
    """
    Root endpoint - API health check
    """
    return {
        "message": "Welcome to SkillMatch API! 🚀",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs_url": "/docs" if settings.ENVIRONMENT != "production" else None,
        "api_prefix": settings.API_V1_STR,
    }



@app.get("/health")
async def health_check():
    """
    Health check monitoring endpoint.
    :return: {
    "status": "ok",
    "timestamp": time.ctime(time.time()),
    }
    """
    return JSONResponse({"status": "ok", "timestamp": time.time()})




if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


