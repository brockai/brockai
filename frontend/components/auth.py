import requests
import streamlit as st
import pandas as pd
import streamlit_antd_components as sac
from services.auth import fetchUser
from authlib.integrations.requests_client import OAuth2Session
from helpers.config import auth0_client_id, auth0_client_secret, auth0_redirect_uri, token_url, domain, scope, response_type

params = st.experimental_get_query_params()
authorization_code = params.get("code", [None])[0]
authorization_state = params.get("state", [None])[0]


def set_redirect(authorization_code, redirect_uri):
    data = {
        "grant_type": "authorization_code",
        "client_id": auth0_client_id,
        "client_secret": auth0_client_secret,
        "redirect_uri": redirect_uri,
        "code": authorization_code,
    }
    return data

def set_oauth(redirect_uri):
    oauth = OAuth2Session(
        client_id=auth0_client_id,
        client_secret=auth0_client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        response_type=response_type,
    )
    return oauth

def navigation(title, authorization_url, icon, tag, signIn): 

    oauth = set_oauth(auth0_redirect_uri)

    if 'access_token' not in st.session_state:
        st.session_state['access_token'] = ''
    
    col1, col2, col3 =  st.columns([2, 3, 1.25])
    with col1:

        title = sac.menu(
            items=[
                sac.MenuItem(title, icon=icon, tag=tag),
                ],
                key=title,
                size=20,
                open_all=True, indent=20,
                format_func='title',
            )

    with col3:
        if st.session_state.access_token == '' and signIn:
            if st.button("🚀&nbsp;Platform&nbsp;Sign&nbsp;In", use_container_width=True):
                authorization_url, state = oauth.create_authorization_url(authorization_url)
                st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{authorization_url}\'" />', unsafe_allow_html=True) 

        if st.session_state.access_token != '':
            if st.button("Platform Sign Out", use_container_width=True):
                st.session_state['access_token'] = ''
                st.session_state['given_name'] = ''
                st.session_state['tenant_id'] = ''    
                st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{domain}\'" />', unsafe_allow_html=True) 

def get_tokens(authorization_code):

    data = set_redirect(authorization_code, auth0_redirect_uri)

    response = requests.post(token_url, data=data)
        
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        st.session_state.access_token = access_token
        user_info = fetchUser(access_token)
        st.session_state.given_name = user_info['given_name']
        st.session_state.tenant_id = user_info['nickname']
            
    return st.session_state
 