from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker, AsyncSession
from app.core.config import settings

# ✅ async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency for fastapi routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
