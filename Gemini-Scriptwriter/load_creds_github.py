import json
import os
import streamlit as st
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow



# Replace 'YOUR_CLIENT_SECRETS_SECRET_NAME' with the actual secret name




def load_creds():
    """Retrieves Google OAuth credentials securely using Streamlit Secrets."""

    try:
        # Access credentials securely from Streamlit Secrets
        client_id = st.secrets["GOOGLE_CLIENT_ID"]
        client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]
        scopes = ['https://www.googleapis.com/auth/generative-language.tuning']  # Adjust scopes as needed

        client_config = {
            'web': {
                'client_id': client_id,
                'client_secret': client_secret,
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://www.googleapis.com/oauth2/v3/token',
                'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
                'redirect_uris': ['http://plotwriter.streamlit.app']  # Adjust redirect URI if needed
            }
        }
        flow = InstalledAppFlow.from_client_config(
            client_config,
            scopes=scopes
        )
        creds = flow.run_local_server(port=0)
        return creds

    except Exception as e:
        st.error(f"Error loading Google OAuth credentials: {e}")
        return None
