import json

import aio_pika

from app.messaging.connection import get_connection


async def publish_email_message(email, subject, body):
    """
    Publish a JSON message to a durable queue using the default exchange.
    """
    connection = await get_connection()
    channel = await connection.channel()

    message = aio_pika.Message(
        body=json.dumps({
            "email": email,
            "subject": subject,
            "body": body
        }).encode(),
        delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
    )

    await channel.default_exchange.publish(
        message,
        routing_key="email_queue",
    )

    print(f"Sent message to email_queue: {body}")
    await connection.close()
