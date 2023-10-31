from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = os.environ.get("DB_PORT")  

SDEK_LOGIN = os.environ.get("SDEK_LOGIN")
SDEK_PASS = os.environ.get("SDEK_PASS")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

SECRET_KEY = os.environ.get("SECRET_AUTH")

SMTP_SECRET = os.environ.get("SMTP_SECRET")
SMTP_USER = os.environ.get("SMTP_USER")