import requests
import streamlit as st
import streamlit_antd_components as sac
import extra_streamlit_components as stx

from services.shared_service import is_index
from services.mappings import  admin_role, tenant_role
from services.platform_service import create_platform_tenant, create_tenant_files, create_platform_settings, create_platform_logs
from helpers.config import domain

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
        set_cookie_value(access_token, True, st.session_state['tenant_id'])
    else:
        set_cookie_value(access_token, False, st.session_state['tenant_id'])


def fetchUser(access_token):
    oauth = OAuth2Session(client_id=auth0_client_id, token={"access_token": access_token})
    user_info = oauth.get(userinfo_url).json()
    return user_info

def set_auth0_redirect(authorization_code, redirect_uri):
    data = {
        "grant_type": "authorization_code",
        "client_id": auth0_client_id,
        "client_secret": auth0_client_secret,
        "redirect_uri": redirect_uri,
        "code": authorization_code,
    }
    return data

def set_auth0_client():
    oauth = OAuth2Session(
        client_id=auth0_client_id,
        client_secret=auth0_client_secret,
        redirect_uri=auth0_redirect_uri,
        scope=scope,
        response_type=response_type,
    )
    return oauth

def signin_button():

    oauth = set_auth0_client()
    authorization_url, state = oauth.create_authorization_url(auth0_authorization_url) 

    if st.button('Sign In', use_container_width=True, ):
        st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{authorization_url}\'" />', unsafe_allow_html=True)

def signout_button():

    if st.button('Sign out', use_container_width=True):
        cookie_manager.delete(auth0_cookie_name)
        st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{domain}\'" />', unsafe_allow_html=True) 
        
def auth_init(authorization_code):
    
    if authorization_code != None:
        data = set_auth0_redirect(authorization_code, auth0_redirect_uri)
        response = requests.post(token_url, data=data)

        if response.status_code == 200:
            access_token = response.json().get("access_token")
            st.session_state['access_token'] = access_token
            user_info = fetchUser(access_token)
    
            st.session_state['tenant_id'] = user_info['nickname']

            roles = tenant_role
            
            if not is_index(st.session_state['tenant_id'], 'platform_logs'):
                create_platform_logs(st.session_state['tenant_id']) 

            if not is_index(st.session_state['tenant_id'], 'platform_settings'):
                create_platform_settings(st.session_state['tenant_id'])
                roles = admin_role

            if not is_index(st.session_state['tenant_id'], 'platform_'+st.session_state['tenant_id']):
                create_platform_tenant(st.session_state['tenant_id'], user_info, roles)

            if not is_index(st.session_state['tenant_id'], 'platform_'+st.session_state['tenant_id']+'_files'):
                create_tenant_files(st.session_state['tenant_id'])

            cookie_value = f"{st.session_state['tenant_id']}"
            cookie_manager.set(auth0_cookie_name, cookie_value)

            return st.session_state['tenant_id']

def set_tenant_role():
    roles = st.session_state['tenant_doc']['roles']
