import streamlit as st
import streamlit_antd_components as sac 
st.set_page_config(layout="wide", page_title="brockai - Platform", page_icon="./static/brockai.png") 

from components.platform_auth import auth_init, cookie_manager, set_tenant_role, signin_button, signout_button
from components.platform_signup import platform_signup
from components.regcheck import regcheck
from components.contact import contact
from components.chat import chat
from components.platform_admin import platform_admin
from components.platform_navigation import navigation, prototype_navigation

from services.shared_service import check_opensearch_health, is_index
from services.tenant_service import get_tenant_doc

from helpers.antd_utils import show_space
from helpers.config import auth0_cookie_name, platform_admin_tenant
from helpers.markdown import sidebar_links_footer, sidebar_app_header, opensearch_platform_button, airflow_button

params = st.query_params.to_dict()

authorization_code = None
authorization_state = None

if len(params) > 0: 
    authorization_code = params["code"]
    authorization_state = params["state"]

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

# stay signed in
cookie = cookie_manager.get(auth0_cookie_name)
if cookie:
    cookie_values = cookie.split('|')
    
    if len(cookie_values) == 3:     
        st.session_state['stay_signed_in'] = True if cookie_values[2].lower() == "true" else False
        
        if st.session_state['stay_signed_in']:
            st.session_state['access_token'] = cookie_values[0]
            st.session_state['tenant_id'] = cookie_values[1]  

admin_disabled = True
if 'tenant_id' in st.session_state:
    admin_disabled = False

    if is_index(st.session_state['tenant_id'], st.session_state['tenant_id']):
        
        if 'tenant_doc' not in st.session_state:
            tenant_doc = get_tenant_doc(platform_admin_tenant)
            
            if len(tenant_doc['hits']['hits']) == 0:
                st.session_state['tenant_doc'] = tenant_doc['hits']['hits'][0]['_source']['mappings']['properties']
                set_tenant_role()

    if 'bread_crumb_index' not in st.session_state:
        st.session_state["bread_crumb_index"] = 1

health, version = check_opensearch_health()

col1, col2 = st.columns([9, 3], gap="medium")

with col1:
    with open('styles.css') as f:
        st.markdown(
            f'<style>{f.read()}</style>'
            +"""<img src="app/static/brockailogo32.png" height="48" alt="Platform">"""
            , unsafe_allow_html=True
        ) 
with col2:
    if 'access_token' not in st.session_state:
        signin_button()
    else:
        signout_button()

pageCol = st.columns([12])
tab1, tab2, tab3, tab4 = st.tabs(["AI Proto Types", "Regulatory Compliancy", "Chat", "Platform"])

with tab1:
    navigation('60 - 90 Day AI Proto Types', 'rocket', None)
    platform_signup()

with tab2:
    navigation('Bill of Materials Regulatory Compliancy', 'shield-check', 'Prototype')
    regcheck()
    
with tab3:
    navigation('General Purpose Chatbot', 'chat-left-text', 'Prototype')
    chat()

with tab4:
    navigation('brockai Platform Services', 'chat-left-text', None)
    st.markdown(opensearch_platform_button, unsafe_allow_html=True)
    show_space(1)

    sac.chip(
        items=[
            sac.ChipItem(label=health),
            sac.ChipItem(label=version),
        ], variant='outline', size='xs', radius="md")


footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        <p>Footer content goes here. &copy; 2024</p>
    </div>
"""



 