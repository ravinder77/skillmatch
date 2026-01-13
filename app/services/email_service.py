from email.mime.text import MIMEText

import aiosmtplib

from app.core.settings import settings


async def send_email(recipient: str, subject: str, body: str):
    """Send the Email to the recipient."""
    message = MIMEText(body)
    message["From"] = settings.SENDER_EMAIL
    message["To"] = recipient
    message["Subject"] = subject

    await aiosmtplib.send(
        message,
        hostname=settings.MAILTRAP_HOST,
        port=settings.MAILTRAP_PORT,
        username=settings.MAILTRAP_USER,
        password=settings.MAILTRAP_PASS,
        start_tls=False,
    )
