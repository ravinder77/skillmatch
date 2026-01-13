import time

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.api_router import api_router
from app.core.settings import settings
from app.core.lifespan import lifespan
from app.core.logging_config import setup_logging
from app.core.middleware import register_middlewares

# load env variables
load_dotenv()

# setup logging
setup_logging()

app = FastAPI(title="Skillmatch Job board api", version="1.0.0", lifespan=lifespan)


# Register Middleware
register_middlewares(app)

# Routers
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


@app.get("/health")
async def health_check():
    """
    Health check monitoring endpoint.
    :return: {
    "status": "ok",
    }
    """
    return JSONResponse({"status": "ok"})


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
