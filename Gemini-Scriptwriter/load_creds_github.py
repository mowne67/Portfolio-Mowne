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
        client_id = st.secrets.client_id
        project_id= st.secrets["project_id"]
        auth_uri= st.secrets["auth_uri"]
        token_uri= st.secrets["token_uri"]
        auth_provider_x509_cert_url= st.secrets["auth_provider_x509_cert_url"]
        client_secret= st.secrets["client_secret"]
        redirect_uris= st.secrets["redirect_uris"]


        client_config = {
            "installed":
                 {"client_id":client_id,
                  "project_id":project_id,
                  "auth_uri":auth_uri,
                  "token_uri":token_uri,
                  "auth_provider_x509_cert_url":auth_provider_x509_cert_url,
                  "client_secret":client_secret,
                  "redirect_uri":"https://plotwriter.streamlit.app"}
        }
        flow = InstalledAppFlow.from_client_config(
            client_config,
            scope="https://www.googleapis.com/auth/generative-language.tuning"
        )
        auth_url, _ = flow.authorization_url(prompt='consent' )
        st.write("Please visit this URL to authorize access:", auth_url)

        # Ask the user to enter the authorization code obtained after authorizing access
        authorization_code = st.text_input("Enter the authorization code: ")
        # Check if the authorization code has been provided
        if authorization_code:
            # Fetch the access token using the authorization code
            flow.fetch_token(code=authorization_code)
            # Get the credentials
            credentials = flow.credentials
            return credentials

        #creds = flow.run_local_server(port=0)


    except Exception as e:
        st.error(f"Error loading Google OAuth credentials: {e}")
        return None
