import asyncio
import json

import aio_pika

from app.core.settings import settings
from app.services.email_service import send_email


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process(ignore_processed=True):
        try:
            data = json.loads(message.body.decode())
            await send_email(
                data["email"],
                data["subject"],
                data["body"]
            )
        except Exception as e:
            print("Error: {}".format(e))


async def start_email_consumer():
    connection = await aio_pika.connect_robust(
        settings.RABBITMQ_URL,
        client_properties={"connection_name": "email_consumer"},
    )
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)  # handle 10 messages at a time

    queue = await channel.declare_queue("email_queue", durable=True)

    await queue.consume(process_message)  # type:ignore[arg-type]
    print("Email consumer running.")

    try:
        await asyncio.Future()
    except asyncio.CancelledError as e:
        print("Email consumer canceled.")
        await connection.close()


if __name__ == "__main__":
    asyncio.run(start_email_consumer())
