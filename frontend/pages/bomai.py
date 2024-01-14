import os
from dotenv import load_dotenv
from authlib.integrations.requests_client import OAuth2Session
import streamlit as st
import pandas as pd

from openai import OpenAI

load_dotenv()

auth0_domain = os.getenv("AUTH0_DOMAIN")
auth0_client_id = os.getenv("AUTH0_CLIENT_ID")
auth0_client_secret = os.getenv("AUTH0_CLIENT_SECRET")

# Authlib configuration
redirect_uri = "http://localhost:8501/BOM%20Compliancy"
scope = "openid profile email"
response_type = "code" 

# Auth0 authorization endpoint
authorization_url = f"{auth0_domain}/authorize"
print(authorization_url)
oauth = OAuth2Session(
    client_id=auth0_client_id,
    client_secret=auth0_client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    response_type=response_type,
)

st.set_page_config(layout="wide", page_title="brockai - BOM Compliancy", page_icon="./static/brockai.png")  

# import logging
# logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
# logging.getLogger("haystack").setLevel(logging.INFO)

from helpers.config import opensearch_platform, scheme, openaikey
from helpers.markdown import sidebar_links_footer, sidebar_app_header, powered_by_openai, platform_link
from services.api import upload

client = OpenAI(api_key=openaikey)   

if "messages_bom" not in st.session_state:
    st.session_state["messages_bom"] = [{"role": "assistant", "content": "Would you like to learn more about how to check your BOM for compliancy?"}]
    
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
    
st.header("💯 BOM Component Compliancy")
with open('styles.css') as f:
    st.markdown(
        f'<style>{f.read()}</style>'
        +powered_by_openai
        , unsafe_allow_html=True
    )

with open('styles.css') as f:
    st.sidebar.markdown(
        f'<style>{f.read()}</style>'
        +sidebar_app_header
        +sidebar_links_footer
        , unsafe_allow_html=True
    )
    
st.sidebar.markdown(platform_link, unsafe_allow_html=True)

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

    # st.redirect(authorization_url)
#   upload()
