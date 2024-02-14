import requests
import streamlit as st
import streamlit_antd_components as sac
import extra_streamlit_components as stx

from services.utils_service import is_index
from services.tenant_service import create_tenant, create_file_index

from authlib.integrations.requests_client import OAuth2Session
from helpers.config import auth0_client_id, auth0_client_secret, auth0_redirect_uri, auth0_authorization_url, token_url, scope, response_type, userinfo_url, auth0_cookie_name

def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()

def set_cookie_value(access_token, stay_signed_in, tenant_id):
    cookie_value = f"{access_token}|{tenant_id}|{stay_signed_in}"
    cookie_manager.set(auth0_cookie_name, cookie_value)
    st.session_state['stay_signed_in'] = stay_signed_in

def stay_signed_in(access_token):

    on = sac.switch(label='Stay Signed In', on_label='On', value=st.session_state['stay_signed_in'], off_label='Off', align='end', size='sm')
    
    if on:
        set_cookie_value(access_token, True, st.session_state.tenant_id)
    else:
        set_cookie_value(access_token, False, st.session_state.tenant_id)


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


def signin_button():

    oauth = set_oauth()
    authorization_url, state = oauth.create_authorization_url(auth0_authorization_url) 

    if st.button('Sign In', use_container_width=True, ):
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
