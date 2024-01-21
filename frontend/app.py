import streamlit as st
st.set_page_config(layout="wide", page_title="brockai - Platform", page_icon="./static/brockai.png") 
from st_pages import Page, show_pages

from components.auth import get_tokens, navigation
from components.platform_beta import beta_email_request

from helpers.config import authorization_url, auth0_redirect_uri

from helpers.markdown import sidebar_links_footer, sidebar_app_header, platform_link

params = st.experimental_get_query_params()
authorization_code = params.get("code", [None])[0]
authorization_state = params.get("state", [None])[0]

if authorization_code != None:
    authMetadata = get_tokens(authorization_code, auth0_redirect_uri)

show_pages([
    Page("app.py", "Platform", "✨"),
    Page("pages/compliancy.py", "Compliancy", "💯"),
    Page("pages/chat.py", "Chat", "🕵️‍♀️"),
    Page("pages/contact.py", "Contact Us", "✉️"),
])

with open('styles.css') as f:
    st.sidebar.markdown(
        f'<style>{f.read()}</style>'
        +sidebar_app_header
        +sidebar_links_footer
        , unsafe_allow_html=True
    )  
    
st.sidebar.markdown(platform_link, unsafe_allow_html=True)

navigation('✨ Platform', authorization_url, auth0_redirect_uri, True)
beta_email_request()
