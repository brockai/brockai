import os
import requests
import streamlit as st
import pandas as pd

from openai import OpenAI
from dotenv import load_dotenv
from authlib.integrations.requests_client import OAuth2Session
from helpers.markdown import sidebar_links_footer, sidebar_app_header, platform_link
from services.api import upload

load_dotenv()

auth0_domain = os.getenv("AUTH0_DOMAIN")
auth0_client_id = os.getenv("AUTH0_CLIENT_ID")
auth0_client_secret = os.getenv("AUTH0_CLIENT_SECRET")
redirect_uri =  os.getenv("AUTH0_REDIRECT_URL")
scope = "openid profile email"
response_type = "code" 
token_url = "https://brockai.us.auth0.com/oauth/token"

authorization_url = f"{auth0_domain}/authorize"

oauth = OAuth2Session(
        client_id=auth0_client_id,
        client_secret=auth0_client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        response_type=response_type,
)

params = st.experimental_get_query_params()
authorization_code = params.get("code", ["none"])[0]
print(authorization_code)
if authorization_code != "none":
    data = {
        "grant_type": "authorization_code",
        "client_id": auth0_client_id,
        "client_secret": auth0_client_secret,
        "redirect_uri": redirect_uri,
        "code": authorization_code,
    }

    # Make a POST request to the token endpoint
    response = requests.post(token_url, data=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print(response)
        # Parse and extract the access token from the response
        access_token = response.json().get("access_token")
        print(f"Access Token: {access_token}")
    else:
        # Handle the error if the request was not successful
        print(f"Token Request Failed: {response.status_code} - {response.text}")

st.set_page_config(layout="wide", page_title="brockai - BOM Compliancy", page_icon="./static/brockai.png")  
    
st.header("💯 BOM Compliancy")

with open('styles.css') as f:
    st.sidebar.markdown(
        f'<style>{f.read()}</style>'
        +sidebar_app_header
        +sidebar_links_footer
        , unsafe_allow_html=True
    )
    
st.sidebar.markdown(platform_link, unsafe_allow_html=True)

if st.button("Login"):
    authorization_url, state = oauth.create_authorization_url(authorization_url)
    st.session_state.auth_state = state
    st.session_state.auth0_logged_in = True
    st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{authorization_url}\'" />', unsafe_allow_html=True)

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    # st.write(bytes_data)

if st.button("🚀 Upload & Process", disabled=not uploaded_files):
    authorization_url, state = oauth.create_authorization_url(authorization_url)
    st.session_state.auth_state = state
    st.session_state.auth0_logged_in = True
    st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{authorization_url}\'" />', unsafe_allow_html=True)

