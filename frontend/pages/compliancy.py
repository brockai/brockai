import requests
import streamlit as st
import pandas as pd
st.set_page_config(layout="wide", page_title="brockai - BOM Compliancy", page_icon="./static/brockai.png")

from helpers.config import authorization_url, auth0_redirect_uri
from helpers.markdown import sidebar_links_footer, sidebar_app_header, platform_link
from services.api import uploadFiles
from st_pages import hide_pages
from components.auth import navigation, set_oauth, get_tokens

params = st.experimental_get_query_params()
authorization_code = params.get("code", [None])[0]
authorization_state = params.get("state", [None])[0]

if "file_uploader_key" not in st.session_state:
    st.session_state["file_uploader_key"] = 0

if "uploaded_files" not in st.session_state:
    st.session_state["uploaded_files"] = []

if authorization_code != None:
    authMetadata = get_tokens(authorization_code, auth0_redirect_uri+'Compliancy')
    
with open('styles.css') as f:
    st.sidebar.markdown(
        f'<style>{f.read()}</style>'
        +sidebar_app_header
        +sidebar_links_footer
        , unsafe_allow_html=True
    )
    
st.sidebar.markdown(platform_link, unsafe_allow_html=True)

# st.write('state',st.session_state)
navigation('💯 Compliancy', authorization_url, auth0_redirect_uri+'Compliancy', False)

if st.session_state.access_token == '':

    st.write("Check components in your Bill of Materials for compliancy. Login with one of the common identity providers and get started for free.")

    if st.button("✨ Platform Sign In"):
        oauth = set_oauth(auth0_redirect_uri+'Compliancy')
        authorization_url, state = oauth.create_authorization_url(authorization_url)
        st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{authorization_url}\'" />', unsafe_allow_html=True) 

files = st.file_uploader(
    "Choose a CSV file", 
    accept_multiple_files=True, 
    type=["txt", "csv"],
    key=st.session_state["file_uploader_key"],
)

if files:
    st.session_state["uploaded_files"] = files
    if st.session_state.access_token != '':
        if st.button("🚀 Upload & Process"):
            for file in files:
                file_name=file.name
                bytes_data = file.getvalue()
                isUpload = uploadFiles(bytes_data, file_name)

            st.session_state["file_uploader_key"] += 1
            st.rerun()