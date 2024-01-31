import requests
import streamlit as st
import pandas as pd
import streamlit_antd_components as sac
# import extra_streamlit_components as stx
from authlib.integrations.requests_client import OAuth2Session
from helpers.config import auth0_client_id, auth0_client_secret, auth0_redirect_uri, auth0_authorization_url, token_url, scope, response_type, domain, userinfo_url

params = st.experimental_get_query_params()
authorization_code = params.get("code", [None])[0]
authorization_state = params.get("state", [None])[0]

# def get_manager():
#     return stx.CookieManager()

# cookie_manager = get_manager()

# def get_cookie():
#     cookie = {"brockai", "init"}
#     cookie_from_browser = cookie_manager.get("brockai")
#     st.write(cookie_manager, 'from get',cookie_from_browser)
#     # return cookie_manager.get("brockai", key="init")

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

oauth = set_oauth()
authorization_url, state = oauth.create_authorization_url(auth0_authorization_url) 

# def navigation(title, icon, tag, show_sigin_button): 

#     # access_token = st.session_state.get("access_token")
    
#     if not show_sigin_button and st.session_state.access_token != None:
#         get_title(title, icon, tag)
#     else:
#         col1, col2 = st.columns([9, 3])
#         with col1:
#             get_title(title, icon, tag)
#         with col2:
#             if show_sigin_button and 'access_token' not in st.session_state:
#                 signin_button()
#             elif st.session_state.access_token:
#                 if st.button('Platform Sign out', use_container_width=True):
#                     st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{domain}\'" />', unsafe_allow_html=True) 
            
def signin_button():
    if st.button('Platform Sign In', use_container_width=True):
        st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{authorization_url}\'" />', unsafe_allow_html=True)

def get_tokens(authorization_code):

    if authorization_code != None:
        data = set_redirect(authorization_code, auth0_redirect_uri)
        response = requests.post(token_url, data=data)

        if response.status_code == 200:
            access_token = response.json().get("access_token")
            st.write('access',access_token)
            st.session_state.access_token = access_token
            user_info = fetchUser(access_token)
            st.session_state.given_name = user_info['given_name']
            st.session_state.tenant_id = user_info['nickname']

            return st.session_state
    else:
        return None
 