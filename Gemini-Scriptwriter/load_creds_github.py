import json
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ['https://www.googleapis.com/auth/generative-language.tuning']

# Replace 'YOUR_CLIENT_SECRETS_SECRET_NAME' with the actual secret name
CLIENT_SECRETS_SECRET_NAME = 'GOOGLE_OAUTH'

# Function to load client_secrets.json from GitHub secrets
def load_client_secrets():
    secret_value = os.environ.get(CLIENT_SECRETS_SECRET_NAME)
    try:
        return json.loads(secret_value)
    except Exception as e:
        print(f"Error loading client_secrets.json from secrets: {e}")
        return None

def load_creds():
    """Retrieves credentials, prioritizing GitHub secrets for security."""
    creds = None

    client_secrets = load_client_secrets()
    if client_secrets:
        try:
            flow = InstalledAppFlow.from_client_config(client_secrets, SCOPES)
            creds = flow.run_local_server(port=0)
        except Exception as e:
            print(f"Error creating flow from client_secrets: {e}")
    # with open('token.json', 'w') as token:
    #     token.write(creds.to_json())
    # Fallback to file-based loading if needed (handle securely for production)
    # ... Rest of the code remains the same ...

    return creds
