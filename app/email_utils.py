# app/email_utils.py

import base64

def fetch_email_ids(service, query, max_results):
    result = service.users().messages().list(
        userId="me", q=query, maxResults=max_results
    ).execute()
    return result.get("messages", [])

def get_message(service, msg_id):
    return service.users().messages().get(userId="me", id=msg_id, format="full").execute()

def parse_message(message):
    payload = message["payload"]
    headers = {h["name"]: h["value"] for h in payload.get("headers", [])}
    body = extract_body(payload)
    return {
        "from": headers.get("From"),
        "subject": headers.get("Subject"),
        "date": headers.get("Date"),
        "body": body,
    }
def is_automated_email(message):
    """
    Checks for headers that indicate an email is automated.
    """
    payload = message.get("payload", {})
    headers = payload.get("headers", [])
    for header in headers:
        name = header.get("name", "").lower()
        if name in ["list-unsubscribe", "precedence", "auto-submitted"]:
            return True
    return False

def get_thread_id(message):
    return message.get("threadId")

def get_formatted_thread_history(service, thread_id):
    """
    Fetches an entire email thread and formats it into a chronological string.
    """
    thread = service.users().threads().get(userId="me", id=thread_id).execute()
    history = []
    for message in thread.get("messages", []):
        parsed_message = parse_message(message)
        sender = parsed_message.get("from", "Unknown Sender")
        body = parsed_message.get("body", "").strip()
        history.append(f"From: {sender}\n---\n{body}\n---")
    
    # Join the history, separated by a clear marker for the LLM
    return "\n\n==== NEXT EMAIL IN THREAD ====\n\n".join(history)

def extract_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part["body"]["data"]
                return base64.urlsafe_b64decode(data).decode()
    else:
        data = payload["body"]["data"]
        return base64.urlsafe_b64decode(data).decode()
    return ""
