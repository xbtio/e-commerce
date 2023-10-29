import asyncio
import aiosmtplib
import sys
from email.message import EmailMessage
from config import SMTP_SECRET, SMTP_USER

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

async def send_verification_token(username: str, to_email: str, token: str):
    email = EmailMessage()
    email['Subject'] = 'Verification token'
    email['From'] = SMTP_USER
    email['To'] = to_email

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Hello, {username}, here is your verification token - {token}</h1>'
        '</div>',
        subtype='html'
    )
    return email

async def send_reset_pass_token(username: str, to_email: str, token: str):
    email = EmailMessage()
    email['Subject'] = 'Reset token'
    email['From'] = SMTP_USER
    email['To'] = to_email

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Hello, {username}, here is your reset token - {token}</h1>'
        '</div>',
        subtype='html'
    )
    return email

async def send_verification_token_to_user(username: str, to_email: str, token: str):
    email = await send_verification_token(username, to_email, token)

    smtp_client = aiosmtplib.SMTP(port=SMTP_PORT, hostname=SMTP_HOST, use_tls=True)

    try:
        await smtp_client.connect()
        await smtp_client.login(SMTP_USER, SMTP_SECRET)
        await smtp_client.send_message(email)
    finally:
        await smtp_client.quit()

async def send_reset_token_to_user(username: str, to_email: str, token: str):
    email = await send_reset_pass_token(username, to_email, token)

    smtp_client = aiosmtplib.SMTP(port=SMTP_PORT, hostname=SMTP_HOST, use_tls=True)

    try:
        await smtp_client.connect()
        await smtp_client.login(SMTP_USER, SMTP_SECRET)
        await smtp_client.send_message(email)
    finally:
        await smtp_client.quit()