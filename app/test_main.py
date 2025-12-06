# tests/test_main.py

from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

def test_generate_email_reply():
    # 1. Create a mock for the Gmail service
    mock_gmail_service = MagicMock()

    # 2. Define a sample raw email message to be returned by the mock service
    # This simulates the response from the Gmail API
    sample_message_id = "12345"
    sample_raw_message = {
        "id": sample_message_id,
        "payload": {
            "headers": [
                {"name": "From", "value": "test@example.com"},
                {"name": "Subject", "value": "Test Subject"},
                {"name": "Date", "value": "Some Date"},
            ],
            "body": {"data": "SGVsbG8gd29ybGQ="} # "Hello world" in base64url
        }
    }

    # 3. Configure the mock to return the sample message
    mock_gmail_service.users().messages().get().execute.return_value = sample_raw_message

    # 4. Use patch to replace get_gmail_service with our mock during the test
    with patch("app.main.get_gmail_service", return_value=mock_gmail_service) as mock_get_service:
        # 5. Make a request to the endpoint
        response = client.post(
            "/generate-reply",
            json={"message_id": sample_message_id}
        )

        # 6. Assert the results
        assert response.status_code == 200
        
        data = response.json()
        assert data["from_email"] == "test@example.com"
        assert data["subject"] == "Test Subject"
        assert data["body"] == "Hello world"
        assert "Hi test@example.com" in data["reply"]
        assert "Thanks for your mail titled 'Test Subject'" in data["reply"]

        # Verify that our mock service was used
        mock_get_service.assert_called_once()
        mock_gmail_service.users().messages().get.assert_called_once_with(userId="me", id=sample_message_id)
