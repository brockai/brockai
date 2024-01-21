import streamlit as st
import requests
from authlib.integrations.requests_client import OAuth2Session
from helpers.config import auth0_client_id, userinfo_url
from helpers.config import auth0_client_id

@st.cache_data(show_spinner=True)
def fetchUser(access_token):
    oauth = OAuth2Session(client_id=auth0_client_id, token={"access_token": access_token})
    user_info = oauth.get(userinfo_url).json()
    return user_info
