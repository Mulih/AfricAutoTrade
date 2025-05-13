import os, asyncio, aiohttp, smtplib
from email.mime.text import MIMEText
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

EMAIL_ADDR = os.getenv("ALERT_EMAIL")
EMAIL_PASS = os.getenv("ALERT_PASS")
TG_TOKEN   = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")