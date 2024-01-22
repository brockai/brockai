import streamlit as st
import streamlit_antd_components as sac 

from st_pages import Page, hide_pages

from components.auth import get_tokens, navigation
from components.platform_beta import beta_email_request
from components.compliancy import compliancy
from components.contact import contact
from components.chat import chat
from helpers.config import authorization_url, auth0_redirect_uri
from helpers.markdown import sidebar_links_footer, sidebar_app_header

params = st.experimental_get_query_params()
authorization_code = params.get("code", [None])[0]
authorization_state = params.get("state", [None])[0]

st.set_page_config(layout="wide", page_title="brockai - Platform", page_icon="./static/brockai.png") 
st.markdown(f'''
    <style>
    .stApp .main .block-container{{
        padding:30px 50px
    }}
    .stApp [data-testid='stSidebar']>div:nth-child(1)>div:nth-child(2){{
        padding-top:50px
    }}
    iframe{{
        display:block;
    }}
    .stRadio div[role='radiogroup']>label{{
        margin-right:5px
    }}
    </style>
    ''', unsafe_allow_html=True)

if authorization_code != None:
    authMetadata = get_tokens(authorization_code)
    st.write(authMetadata)

with st.sidebar.container():

    # tag
    modified = sac.Tag('Modified', color='blue', bordered=False)
    protoType = sac.Tag('Prototype', color='green', bordered=False)
    deprecated = sac.Tag('Deprecated', color='orange', bordered=False)
    production = sac.Tag('Production', color='red', bordered=False)
    beta = sac.Tag('Beta', color='purple', bordered=False)

    menu = sac.menu(
        items=[
            sac.MenuItem('platform', icon='rocket', tag=beta),
            sac.MenuItem('regcheck', icon='shield-check', tag=protoType),
            sac.MenuItem('chat', icon='chat-left-text',tag=protoType),
            sac.MenuItem('contact', icon='envelope',)
        ],
        key='menu',
        open_all=True, indent=10,
        format_func='title',
    )
    sac.divider('Docs & Jupyter Notebooks', color='gray')
    with open('styles.css') as f:
        st.sidebar.markdown(
            f'<style>{f.read()}</style>'
            +sidebar_app_header
            +sidebar_links_footer
            , unsafe_allow_html=True
        ) 

with st.container():
    
    if menu == 'regcheck':
        navigation('regcheck', authorization_url, 'shield-check', protoType, False)
        compliancy()
    elif menu == 'chat':
        navigation('chat', authorization_url, 'chat-left-text', protoType, True)
        chat()
    elif menu == 'contact':
        navigation('contact', authorization_url, 'envelope', None, True)
        contact()
    else:
        navigation('platform', authorization_url, 'rocket', beta, True)
        beta_email_request()
