from typing import Optional

import aio_pika

from app.core.settings import settings

# Optional: A global connection to reuse
_connection: Optional[aio_pika.RobustConnection] = None


async def get_connection():
    """
    Get or create a robust connection to RabbitMQ
    Reuses the connection if it already exists
    """
    global _connection

    # Only reuse if it exists and is open
    if _connection is not None and not _connection.is_closed:
        return _connection

    _connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    return _connection
