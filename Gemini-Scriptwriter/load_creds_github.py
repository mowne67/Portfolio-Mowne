import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ['https://www.googleapis.com/auth/generative-language.tuning']

# Replace 'YOUR_CLIENT_SECRETS_SECRET_NAME' with the actual secret name
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


    return creds
