import base64
import json
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib import request

from pydantic import BaseModel, Field
from ibm_watsonx_orchestrate.agent_builder.connections import (
    ConnectionType,
    ExpectedCredentials,
)
from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool


class SendAssessmentOutcomeEmailInput(BaseModel):
    to: str = Field(description="Recipient email address.")
    subject: str = Field(description="Email subject.")
    body: str = Field(description="Plain text email body.")
    transcript_text: str = Field(
        default="",
        description="Conversation transcript or evidence summary to attach as a text file.",
    )
    transcript_filename: str = Field(
        default="psvar-assessment-transcript.txt",
        description="Filename for the transcript attachment.",
    )


class SendAssessmentOutcomeEmailOutput(BaseModel):
    sent: bool = Field(description="Whether the email was sent successfully.")
    to: str = Field(description="Recipient email address.")
    subject: str = Field(description="Email subject.")
    gmail_message_id: str = Field(description="Gmail API message id if available.")
    status: str = Field(description="Outcome status message.")


@tool(
    permission=ToolPermission.READ_ONLY,
    expected_credentials=[
        ExpectedCredentials(
            app_id="gmail_connection",
            type=ConnectionType.OAUTH2_AUTH_CODE,
        )
    ],
)
def send_assessment_outcome_email(
    email: SendAssessmentOutcomeEmailInput,
    credentials: dict,
) -> SendAssessmentOutcomeEmailOutput:
    """
    Send a PSVAR assessment outcome email using the Gmail API.
    """
    access_token = credentials.get("access_token")
    if not access_token:
        raise ValueError("Missing Gmail access token in injected credentials.")

    message = MIMEMultipart()
    message["to"] = email.to
    message["subject"] = email.subject
    message.attach(MIMEText(email.body, "plain"))

    if email.transcript_text:
        transcript_attachment = MIMEApplication(
            email.transcript_text.encode("utf-8"),
            _subtype="octet-stream",
        )
        transcript_attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename=email.transcript_filename,
        )
        message.attach(transcript_attachment)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    payload = json.dumps({"raw": raw_message}).encode("utf-8")

    gmail_request = request.Request(
        url="https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        data=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(gmail_request) as response:
            response_body = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Failed to send Gmail message: {exc}") from exc

    return SendAssessmentOutcomeEmailOutput(
        sent=True,
        to=email.to,
        subject=email.subject,
        gmail_message_id=response_body.get("id", ""),
        status="Email sent successfully.",
    )

# Made with Bob