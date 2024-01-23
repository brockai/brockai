import requests
import streamlit as st
import pandas as pd
import streamlit_antd_components as sac
from services.auth import fetchUser
from authlib.integrations.requests_client import OAuth2Session
from helpers.config import auth0_client_id, auth0_client_secret, auth0_redirect_uri, token_url, domain, scope, response_type, opensearch_platform
from helpers.markdown import opensearch_platform_button

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
    
    col1, col2, col3 =  st.columns([0.75, 0.25, 2])
    with col1:

        title = sac.menu(
            items=[
                sac.MenuItem(title, icon=icon, tag=tag),
                ],
                key=title,
                open_all=True, indent=20,
                format_func='title'
            )

    with col3:
        if st.session_state.access_token == '' and signIn:
            authorization_url, state = oauth.create_authorization_url(authorization_url)
            sac.buttons([
                sac.ButtonsItem(label='Platform Sign In', icon='rocket', href=authorization_url)
            ], align='end', size='xs')

        if st.session_state.access_token != '':
            sac.buttons([
                sac.ButtonsItem(label='Platform Sign Out', icon='rocket', href=domain)
            ], align='end', size='xs')
        

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
 
   