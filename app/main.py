# app/main.py

from fastapi import FastAPI, HTTPException
from .gmail_service import get_gmail_service, create_reply_message, send_message
from .email_utils import fetch_email_ids, get_message, parse_message, is_automated_email, get_thread_id, get_formatted_thread_history
from .llm_service import generate_reply
from .models import EmailResponse, EmailReplyRequest, SendEmailRequest
from .settings import LABEL_UNREAD, MAX_EMAILS

class EmailDetails(EmailResponse):
    message_id: str

app = FastAPI(title="Email Reply Bot")


@app.get("/emails", response_model=list[EmailResponse])
def get_unread_emails():
    svc = get_gmail_service()
    messages = fetch_email_ids(svc, LABEL_UNREAD, MAX_EMAILS)

    email_list = []
    for msg in messages:
        raw_msg = get_message(svc, msg["id"])

        # Filter out automated emails before processing them further
        if is_automated_email(raw_msg):
            continue

        parsed = parse_message(raw_msg)
        # Add message_id to the parsed data for the response
        parsed_with_id = parsed | {"message_id": msg["id"]}
        email_list.append(EmailDetails(**parsed_with_id))

    return email_list

@app.post("/generate-reply", response_model=EmailResponse)
def generate_email_reply(request: EmailReplyRequest):
    svc = get_gmail_service()
    raw_msg = get_message(svc, request.message_id)
    thread_id = get_thread_id(raw_msg)

    # Get the full conversation history
    conversation_history = get_formatted_thread_history(svc, thread_id)
    
    # We still parse the last message to get sender/subject for the reply context
    last_message_parsed = parse_message(raw_msg)
    last_message_parsed["reply"] = generate_reply(conversation_history, last_message_parsed.get("from"), last_message_parsed.get("subject"))
    return EmailResponse(**last_message_parsed)

@app.post("/send-reply")
def send_email_reply(request: SendEmailRequest):
    try:
        svc = get_gmail_service()
        raw_msg = get_message(svc, request.message_id)
        thread_id = get_thread_id(raw_msg)
        
        # The "sender" for the reply is our own email address, which we can get from the profile
        profile = svc.users().getProfile(userId="me").execute()
        my_email = profile.get("emailAddress")

        reply_message = create_reply_message(my_email, request.to, request.subject, request.body, thread_id)
        send_message(svc, reply_message)
        return {"status": "success", "message": "Reply sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
