
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup & shutdown events for SkillMatch API"""
    init_db()
    print("✅ Starting SkillMatch Backend API")
    yield
    print("🛑 Stopping SkillMatch Backend API")
