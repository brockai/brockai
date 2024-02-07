import requests
import streamlit as st
import pandas as pd
import streamlit_antd_components as sac
import extra_streamlit_components as stx
from services.opensearch import create_tenant, is_index, create_file_index

from authlib.integrations.requests_client import OAuth2Session
from helpers.config import auth0_client_id, auth0_client_secret, auth0_redirect_uri, auth0_authorization_url, token_url, scope, response_type, userinfo_url, auth0_cookie_name, domain

def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()

def set_cookie_value(access_token, stay_signed_in, tenant_id):
    cookie_value = f"{access_token}|{tenant_id}|{stay_signed_in}"
    cookie_manager.set(auth0_cookie_name, cookie_value)
    st.session_state['stay_signed_in'] = stay_signed_in

def stay_signed_in(access_token):

    cookie = cookie_manager.get(auth0_cookie_name)
    
    if cookie != None:
        cookie_values = cookie.split('|')
    
        if len(cookie_values) == 2:
            toggle_value = False
        else:
            toggle_value = True if cookie_values[2].lower() == "true" else False
    else:
        toggle_value = False

    on = st.toggle('Stay Signed In', value=toggle_value)
    
    if on:
        set_cookie_value(access_token, True, st.session_state.tenant_id)
    else:
        set_cookie_value(access_token, False, st.session_state.tenant_id)

def navigation(title, icon, tag, show_signin_button): 

    access_token = st.session_state.get("access_token")

    if access_token == {}:
        access_token = None

    col1, col2 = st.columns([9, 3])
    if access_token == None:
        if not show_signin_button: 
            get_title(title, icon, tag)
        else:
            with col1:
                get_title(title, icon, tag)
            with col2:
                signin_button()
    else:
        with col1:
            get_title(title, icon, tag)
            stay_signed_in(access_token)
            
        with col2:
            if st.button('Platform Sign out', use_container_width=True, disabled=st.session_state['stay_signed_in']):
                cookie_manager.delete(auth0_cookie_name)
                st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{domain}\'" />', unsafe_allow_html=True) 

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

def auth_init(authorization_code):
    
    if authorization_code != None:
        data = set_redirect(authorization_code, auth0_redirect_uri)
        response = requests.post(token_url, data=data)

        if response.status_code == 200:
            access_token = response.json().get("access_token")
            st.session_state.access_token = access_token
            user_info = fetchUser(access_token)
    
            st.session_state.tenant_id = user_info['nickname']

            if not is_index(st.session_state.tenant_id):
                create_tenant(user_info)

            if not is_index(st.session_state.tenant_id+'_files'):
                create_file_index()

            cookie_value = f"{access_token}|{st.session_state.tenant_id}"
            cookie_manager.set(auth0_cookie_name, cookie_value)
    else:
        return None

