# app/models.py

from pydantic import BaseModel, Field

class Reply(BaseModel):
    subject: str
    body: str

class EmailResponse(BaseModel):
    from_email: str = Field(alias="from")
    subject: str
    body: str
    message_id: str | None = None
    reply: Reply | None = None

class EmailReplyRequest(BaseModel):
    message_id: str

class SendEmailRequest(BaseModel):
    message_id: str
    to: str
    subject: str
    body: str
