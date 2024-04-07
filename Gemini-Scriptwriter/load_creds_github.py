import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ['https://www.googleapis.com/auth/generative-language.tuning']

# Replace 'YOUR_SECRET_NAME' with the actual name of your GitHub secret
SECRET_NAME = 'GOOGLE_OAUTH'

def load_creds():
    """Retrieves credentials, prioritizing GitHub secrets for security."""
    creds = None

    # Prioritize secure retrieval from GitHub secrets if available
    secret_value = os.environ.get(SECRET_NAME)
    if secret_value:
        try:
            creds = Credentials.from_authorized_user_info(secret_value, SCOPES)
            return creds  # Use credentials directly from secrets
        except Exception as e:  # Handle potential errors with secret format
            print(f"Error loading credentials from GitHub secrets: {e}")

    # Fallback to file-based loading if secrets retrieval fails
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Handle missing or invalid credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Note: You'll need a secure way to provide client_secret.json
            #       in a production environment, avoiding direct storage in code.
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

            # Save credentials for future use (optional for GitHub Actions)
            try:
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f"Error saving credentials to file: {e}")

    return creds
