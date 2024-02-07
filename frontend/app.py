import streamlit as st
import streamlit_antd_components as sac 
import extra_streamlit_components as stx

from authlib.integrations.requests_client import OAuth2Session
from components.auth import auth_init
from components.platform_signup import platform_signup
from components.compliancy import compliancy
from components.contact import contact
from components.chat import chat
from components.auth import signin_button

from services.opensearch import check_opensearch_health, is_index, tenant_doc, tenant_files


from helpers.antd_utils import show_space
from helpers.config import auth0_client_id, auth0_client_secret, auth0_redirect_uri, auth0_authorization_url, scope, response_type, domain, auth0_cookie_name
from helpers.markdown import sidebar_links_footer, sidebar_app_header, opensearch_platform_button, jupyter_button

params = st.experimental_get_query_params()
authorization_code = params.get("code", [None])[0]
authorization_state = params.get("state", [None])[0]

def set_oauth():
    oauth = OAuth2Session(
        client_id=auth0_client_id,
        client_secret=auth0_client_secret,
        redirect_uri=auth0_redirect_uri,
        scope=scope,
        response_type=response_type,
    )
    return oauth

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

def get_manager():
    return stx.CookieManager()

def set_cookie_value(access_token, stay_signed_in, tenant_id):
    cookie_value = f"{access_token}|{tenant_id}|{stay_signed_in}"
    cookie_manager.set(auth0_cookie_name, cookie_value)
    st.session_state['stay_signed_in'] = stay_signed_in

def stay_signed_in():
    if cookie:
        cookie_values = cookie.split('|')
    
        if len(cookie_values) == 2:
            toggle_value = False
            access_token = cookie_values[0]
            tenant_id = cookie_values[1]
        else:
            toggle_value = True if cookie_values[2].lower() == "true" else False
            access_token = cookie_values[0]
            tenant_id = cookie_values[1]
    else:
        toggle_value = False

    on = st.toggle('Stay Signed In', value=toggle_value)
    
    if on:
        set_cookie_value(access_token, True, tenant_id)
    else:
        set_cookie_value(access_token, False, tenant_id)
    
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
            stay_signed_in()
        with col2:
            if st.button('Platform Sign out', use_container_width=True, disabled=st.session_state['stay_signed_in']):
                cookie_manager.delete(auth0_cookie_name)
                st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{domain}\'" />', unsafe_allow_html=True) 

oauth = set_oauth()
authorization_url, state = oauth.create_authorization_url(auth0_authorization_url) 

auth_init(authorization_code)

cookie_manager = get_manager()

cookie = cookie_manager.get(auth0_cookie_name)

# stay signed in
if cookie:
    cookie_values = cookie.split('|')
    
    if len(cookie_values) == 3:     
        stay_signed_in_value = True if cookie_values[2].lower() == "true" else False
        
        if stay_signed_in_value:
            st.session_state.access_token = cookie_values[0]
            st.session_state.tenant_id = cookie_values[1]       

# set redirect from onboarding app
if 'tenant_id' in st.session_state:
    if is_index(st.session_state['tenant_id']):
        
        tenant_doc = tenant_doc()
        if tenant_doc:
            st.session_state['tenant_doc'] = tenant_doc
            st.session_state['app_redirects'] = (st.session_state['tenant_doc']['hits']['hits'][0]['_source']['mappings']['properties']['app_redirects']['app_redirects'])
        
        tenant_files = tenant_files()
        if tenant_files:
            st.session_state['tenant_files'] = tenant_files['hits']

    else:
        st.session_state['app_redirect'] = None
else:
    st.session_state['app_redirect'] = None

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
            sac.MenuItem('platform', icon='rocket', tag=alpha),
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
        compliancy()
    elif menu == 'chat':
        navigation('chat', 'chat-left-text', protoType, True)
        chat()
    elif menu == 'contact':
        navigation('contact', 'envelope', None, True)
        contact()
    else:
        navigation('platform', 'rocket', alpha, True)

        if 'app_redirects' in st.session_state:
            redirect_compliancy = [item for item in st.session_state['app_redirects'] if item.get('name') == 'compliancy']
            
            if len(redirect_compliancy) == 1:
                hits = st.session_state['tenant_files']['hits']

                if len(hits) > 0:
                    st.session_state['current_step_index'] = 1

                compliancy()
            else:
                platform_signup()
        else:
            platform_signup()
