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
        secrets = st.secrets
        # client_id = st.secrets["GOOGLE_CLIENT_ID"]
        # client_secret = st.secrets["GOOGLE_CLIENT_SECRET"]

        client_config = {
            'web': secrets
        }
        flow = InstalledAppFlow.from_client_config(
            client_config,
            scopes=secrets['scopes']
        )
        creds = flow.run_local_server(port=0)
        return creds

    except Exception as e:
        st.error(f"Error loading Google OAuth credentials: {e}")
        return None
