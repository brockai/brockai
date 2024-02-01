import requests
import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

from authlib.integrations.requests_client import OAuth2Session
from helpers.config import auth0_client_id, auth0_client_secret, auth0_redirect_uri, auth0_authorization_url, token_url, scope, response_type, domain, userinfo_url

params = st.experimental_get_query_params()
authorization_code = params.get("code", [None])[0]
authorization_state = params.get("state", [None])[0]

def fetchUser(access_token):
    oauth = OAuth2Session(client_id=auth0_client_id, token={"access_token": access_token})
    user_info = oauth.get(userinfo_url).json()
    return user_info

def set_redirect(authorization_code, redirect_uri):
    data = {
        "grant_type": "authorization_code",
        "client_id": auth0_client_id,
        "client_secret": auth0_client_secret,
        "redirect_uri": redirect_uri,
        "code": authorization_code,
    }
    return data

def set_oauth():
    oauth = OAuth2Session(
        client_id=auth0_client_id,
        client_secret=auth0_client_secret,
        redirect_uri=auth0_redirect_uri,
        scope=scope,
        response_type=response_type,
    )
    return oauth

def get_title(title, icon, tag):
    title = sac.menu(
        items=[
            sac.MenuItem(title, icon=icon, tag=tag)
            ],
            key=title,
            open_all=True, indent=20,
            format_func='title'
    )
    return title

def signin_button():

    oauth = set_oauth()
    authorization_url, state = oauth.create_authorization_url(auth0_authorization_url) 

    if st.button('Platform Sign In', use_container_width=True):
        st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{authorization_url}\'" />', unsafe_allow_html=True)

def get_tokens(authorization_code):

    if authorization_code != None:
        data = set_redirect(authorization_code, auth0_redirect_uri)
        response = requests.post(token_url, data=data)

        if response.status_code == 200:
            access_token = response.json().get("access_token")
            st.session_state.access_token = access_token
            user_info = fetchUser(access_token)
            st.session_state.given_name = user_info['given_name']
            st.session_state.tenant_id = user_info['nickname']

            return st.session_state
            # cookie_data = {
            #     'access_token': access_token, 'given_name': user_info['given_name'], 'tenant_id': user_info['nickname']
            # }

            # return cookie_data
    else:
        return None
 