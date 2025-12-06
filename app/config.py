# app/config.py
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

class Config:
    GMAIL_CLIENT_ID = os.getenv("GMAIL_CLIENT_ID")
    GMAIL_CLIENT_SECRET = os.getenv("GMAIL_CLIENT_SECRET")
    GMAIL_REFRESH_TOKEN = os.getenv("GMAIL_REFRESH_TOKEN")
