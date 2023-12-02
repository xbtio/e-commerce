import asyncio
import aiosmtplib
import smtplib
from email.message import EmailMessage
from config import SMTP_SECRET, SMTP_USER, REDIS_HOST, REDIS_PORT
from celery import Celery

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


def verification_token(username: str, to_email: str, token: str):
    email = EmailMessage()
    email['Subject'] = 'Verification token'
    email['From'] = SMTP_USER
    email['To'] = to_email

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Hello, {username}, here is your verification token - http://localhost:5173/auth/verify-token/{token}</h1>'
        '</div>',
        subtype='html'
    )
    return email

def reset_pass_token(username: str, to_email: str, token: str):
    email = EmailMessage()
    email['Subject'] = 'Reset token'
    email['From'] = SMTP_USER
    email['To'] = to_email

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Hello, {username}, here is your reset token - http://localhost:5173/auth/reset-password/{token}</h1>'
        '</div>',
        subtype='html'
    )
    return email

@celery.task
def send_verification_token_to_user_sync(username: str, to_email: str, token: str):
    email = verification_token(username, to_email, token)  # Assuming a synchronous function for generating the email

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_SECRET) # type: ignore
        server.send_message(email)
    
        
@celery.task
def send_reset_token_to_user_sync(username: str, to_email: str, token: str):
    email = reset_pass_token(username, to_email, token)  # Assuming a synchronous function for generating the email

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_SECRET) # type: ignore
        server.send_message(email)