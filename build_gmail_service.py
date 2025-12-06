from pathlib import Path
import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

# load .env from repo root
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def generate_refresh_token():
    """
    Generates a new refresh token using the OAuth 2.0 web flow.
    """
    client_id = os.getenv("GMAIL_CLIENT_ID")
    client_secret = os.getenv("GMAIL_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError("GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET must be set in .env")

    # Create a client_config dictionary for the flow
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    flow = InstalledAppFlow.from_client_config(client_config, scopes=SCOPES)
    creds = flow.run_local_server(port=0)

    print("\n--- New Refresh Token ---")
    print(creds.refresh_token)
    print("\nCopy the token above and paste it into your .env file for GMAIL_REFRESH_TOKEN.")

if __name__ == "__main__":
    generate_refresh_token()