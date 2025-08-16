"""
SkillMatch Backend API
A FastAPI application for tracking developer skills, projects,
and generating AI-powered portfolio suggestions.
"""

import time
import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.api.v1 import api_router
from app.core.config import settings
from app.core.middleware import register_middlewares
from app.core.lifespan import lifespan
from app.db.session import engine

app = FastAPI(lifespan=lifespan)

# Register Middleware
register_middlewares(app)


#Routers
app.include_router(api_router, prefix=settings.API_V1_STR)


# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    handle global exceptions
    """
    message = (
        "Internal Server Error" if settings.ENVIRONMENT == "production" else str(exc)
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": message,
            "type": "InternalServerError",
            "path": request.url.path,
            "timestamp": time.time(),
        },
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

@app.get("/db-check")
def db_check():
    try:
      with engine.connect() as conn:
         result = conn.execute(text("SELECT 1"))
         print("SQLite connected successfully:", result.fetchone())
    except Exception as e:(
        print("SQLite connection failed:", e))


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
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
