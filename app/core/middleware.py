import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import FastAPI, Request
from app.core.config import settings




async def logging_middleware( request: Request, call_next ):
    """
    Logs method, path and execution time for each request
    """
    start_time = time.time()
    method = request.method
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000

    status_code = response.status_code

    print(f"{method}/{request.url.path}-{status_code}-{process_time:.2f}ms")
    return response


def register_middlewares(app: FastAPI) -> None:
    """
    Register all application middleware
    """
    app.middleware("http")(logging_middleware)

    # Middleware: CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
    )

    # Add trusted host middleware for production
    if settings.ENVIRONMENT.lower() == "production":
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.ALLOWED_HOSTS,
        )




