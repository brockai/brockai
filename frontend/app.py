import streamlit as st
import streamlit_antd_components as sac 
st.set_page_config(layout="wide", page_title="brockai - Platform", page_icon="./static/brockai.png") 

from components.platform_auth import auth_init, cookie_manager
from components.platform_signup import platform_signup
from components.regcheck import regcheck
from components.contact import contact
from components.chat import chat
from components.platform_navigation import navigation, prototype_navigation

from services.utils_service import check_opensearch_health, is_index
from services.tenant_service import get_tenant_doc, get_tenant_files

from helpers.antd_utils import show_space
from helpers.config import auth0_cookie_name
from helpers.markdown import sidebar_links_footer, sidebar_app_header, opensearch_platform_button, jupyter_button


params = st.experimental_get_query_params()
authorization_code = params.get("code", [None])[0]
authorization_state = params.get("state", [None])[0]

# initlalize Auth0 client
auth_init(authorization_code)

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

def set_nav(title, icon, tag, show_login_button):
    navigation(title, icon, tag, show_login_button)

# stay signed in
cookie = cookie_manager.get(auth0_cookie_name)
if cookie:

    cookie_values = cookie.split('|')
    
    if len(cookie_values) == 3:     
        st.session_state['stay_signed_in'] = True if cookie_values[2].lower() == "true" else False
        
        if st.session_state['stay_signed_in']:
            st.session_state['access_token'] = cookie_values[0]
            st.session_state['tenant_id'] = cookie_values[1]  

# set redirect from onboarding app
if 'tenant_id' in st.session_state:
    if is_index(st.session_state['tenant_id']):
        
        if 'tenant_doc' not in st.session_state:
            tenant_doc = get_tenant_doc()
            if tenant_doc:
                st.session_state['tenant_doc'] = tenant_doc
                st.session_state['app_redirects'] = (st.session_state['tenant_doc']['hits']['hits'][0]['_source']['mappings']['properties']['app_redirects']['app_redirects'])
            
        if 'tenant_files' not in st.session_state:    
            tenant_files = get_tenant_files()
            if tenant_files:
                st.session_state['tenant_files'] = tenant_files['hits']

health, version = check_opensearch_health()

with st.sidebar.container():

    if 'menu_index' not in st.session_state:
        st.session_state['menu_index'] = 0

    upload = sac.Tag('Upload Files', color='blue', bordered=False)
    modified = sac.Tag('Modified', color='blue', bordered=False)
    protoType = sac.Tag('Prototype', color='green', bordered=False)
    deprecated = sac.Tag('Deprecated', color='orange', bordered=False)
    production = sac.Tag('Production', color='red', bordered=False)
    beta = sac.Tag('Beta', color='purple', bordered=False)
    alpha = sac.Tag('Alpha', color='purple', bordered=False)

    menu = sac.menu([
            sac.MenuItem('prototypes', icon='rocket'),
            sac.MenuItem('regcheck', icon='shield-check', tag=protoType),
            sac.MenuItem('chat', icon='chat-left-text',tag=protoType),
            sac.MenuItem('contact', icon='envelope',)
        ],
        key='menu',
        index=st.session_state['menu_index'],
        open_all=True, indent=10,
        format_func='title',
    )

    sac.divider('☁️ OpenSearch', color='gray')
    st.markdown(opensearch_platform_button, unsafe_allow_html=True)
    show_space(1)
    
    sac.chip(
        items=[
            sac.ChipItem(label=health),
            sac.ChipItem(label=version),
        ], variant='outline', size='xs', radius="md")
    
    sac.divider('☁️ Jupyter Lab', color='gray')
    st.markdown(jupyter_button, unsafe_allow_html=True)

    show_space(1)
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
        navigation('regcheck', 'shield-check', protoType, False)
        regcheck()
    elif menu == 'chat':
        navigation('chat', 'chat-left-text', protoType, True)
        chat()
    elif menu == 'contact':
        navigation('contact', 'envelope', None, True)
        contact()
    else:
        if 'access_token' not in st.session_state:
            navigation('prototypes', 'rocket', None, True)
            platform_signup()
        else:
            if "stay_signed_in" not in st.session_state:
                st.session_state["stay_signed_in"] = False

            if 'bread_crumb_index' not in st.session_state:
                st.session_state["bread_crumb_index"] = 1

            st.session_state["bread_crumb_index"] = prototype_navigation()
            
            if st.session_state["bread_crumb_index"] == 1:
                get_title('regcheck', 'shield-check', protoType)
                regcheck()

            if st.session_state["bread_crumb_index"] == 2:
                get_title('chat', 'chat-left-text', protoType)
                chat()

 