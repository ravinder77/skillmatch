import json

import aio_pika

from app.messaging.connection import get_connection


async def publish_message(queue_name: str, message: dict):
    """
    Publish a json message to a durable queue using the default exchange.
    """
    connection = await get_connection()
    channel = await connection.channel()

    # Ensure queue exists and is durable
    queue = await channel.declare_queue(queue_name, durable=True)

    # convert message to json
    body = json.dumps(message).encode()

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=body,
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,  # ensures message is saved to disk,
        ),
        routing_key=queue.name,
    )
    print(f"Sent message to {queue.name}: {body}")
    await channel.close()
