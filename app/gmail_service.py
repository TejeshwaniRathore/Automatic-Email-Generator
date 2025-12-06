# app/gmail_service.py

import os
import base64
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def get_gmail_service():
    client_id = os.getenv("GMAIL_CLIENT_ID")
    client_secret = os.getenv("GMAIL_CLIENT_SECRET")
    refresh_token = os.getenv("GMAIL_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        raise RuntimeError("Missing Gmail credentials in .env file")

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES,
    )
    creds.refresh(Request())
    return build("gmail", "v1", credentials=creds)

def create_reply_message(sender, to, subject, message_text, thread_id):
    """Create a message for an email."""
    message = MIMEText(message_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw_message, "threadId": thread_id}

def send_message(service, message):
    """Send an email message."""
    try:
        message = service.users().messages().send(userId="me", body=message).execute()
        print(f'Message Id: {message["id"]}')
        return message
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
