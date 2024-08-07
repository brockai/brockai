import streamlit as st
st.set_page_config(layout="wide", page_title="brockai - Platform", page_icon="./static/brockai.png") 

from components.platform_auth import auth_init, cookie_manager, set_tenant_role, signin_button, signout_button
from components.platform_signup import platform_signup
from components.regcheck import regcheck
from components.chat import chat
from components.platform_admin import platform_admin

from services.shared_service import check_opensearch_health, is_index
from services.tenant_service import get_tenant_doc

from helpers.config import auth0_cookie_name, platform_admin_tenant
from helpers.markdown import opensearch_platform_button
from streamlit_extras.tags import tagger_component
from streamlit_option_menu import option_menu
from openai import OpenAI
from streamlit_card import card

params = st.query_params.to_dict()

authorization_code = None
authorization_state = None

if len(params) > 0: 
    authorization_code = params["code"]
    authorization_state = params["state"]

    # initlalize Auth0 client
    tenant_id = auth_init(authorization_code)
    st.session_state['tenant_id'] = tenant_id

    admin_disabled = False

    if is_index(st.session_state['tenant_id'], st.session_state['tenant_id']):
        
        if 'tenant_doc' not in st.session_state:
            tenant_doc = get_tenant_doc(platform_admin_tenant) 

            if len(tenant_doc['hits']['hits']) == 0:
                st.session_state['tenant_doc'] = tenant_doc['hits']['hits'][0]['_source']['mappings']['properties']
                set_tenant_role()

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

cookie = cookie_manager.get(auth0_cookie_name)
if cookie:
    cookie_values = cookie.split('|')
    st.session_state['tenant_id'] = cookie_values[0] 

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
    if 'tenant_id' not in st.session_state:
        signin_button()
    else:
        signout_button()

pageCol = st.columns([12])

# options=["Apps", "Regulatory Compliancy", "Chat", "Platform"],
# icons=["app-indicator", "shield-check", "chat-dots", "layers"],
selected = option_menu(
    menu_title=None,
    options=["Apps", "Regulatory Compliancy", "Platform"],
    icons=["app-indicator", "shield-check",  "layers"],
    orientation="horizontal",
)


# Display content based on the selected tab
if selected == "Apps":
    
    hasClicked = card(
        title="Mobile Fuel Delivery",
        text="Click to Learn More",
        # image="http://placekitten.com/200/300",
        url="https://github.com/brockai"
    )

    # st.link_button("Birch Mountain Enterprises Fuel", "https://bme.brockai.com/")
    st.markdown('<h5>Our Stack</h5>', unsafe_allow_html=True)
    st.markdown('''
        - **Frontend:** React/NextJS/TailwindCSS/Streamlit
        - **Server:** NodeJS/Geotab
        - **Database:** OpenSearch
        ''', unsafe_allow_html=True)
    
    st.link_button("Learn More", "https://github.com/brockai/brockai/wiki")
   
    st.markdown('<h5>Future-proof AI applications with OpenSearch</h5>', unsafe_allow_html=True)

    st.link_button("Learn More", "https://opensearch.org/platform/search/vector-database.html")
    st.subheader('Contact')
    platform_signup()

elif selected == "Regulatory Compliancy":
    regcheck()

# elif selected == "Chat":
#     st.title("Chat")
#     chat()

elif selected == "Platform":
    col1, col2 = st.columns([10, 2], gap="medium")
    with col1:
        tagger_component('OpenSearch', [health, version])
    with col2:
        st.markdown(opensearch_platform_button, unsafe_allow_html=True)

    if 'tenant_id' in st.session_state:
        platform_admin()
    
    if 'tenant_id' not in st.session_state:
        st.text('Please Sign In')


# tab1, tab2, tab3, tab4 = st.tabs(["Apps", "Regulatory Compliancy", "Chat", "Platform"])

# with tab1:
#     st.link_button("Birch Mountain Enterprises Fuel Delivery App", "https://bme.brockai.com/")
#     st.markdown('<h5>Our Stack</h5>', unsafe_allow_html=True)
#     st.markdown('''
#         - **Frontend:** React/NextJS/TailwindCSS/Streamlit
#         - **Server:** NodeJS/Geotab
#         - **Database:** OpenSearch
#         ''', unsafe_allow_html=True)
   
#     st.markdown('<h5>Future-proof AI applications with OpenSearch</h5>', unsafe_allow_html=True)

#     st.link_button("Learn More", "https://opensearch.org/platform/search/vector-database.html")
#     st.subheader('Contact')
#     platform_signup()

# with tab2:
#     regcheck()
    
# with tab3:
#     chat()

# with tab4:
#     col1, col2 = st.columns([10, 2], gap="medium")
#     with col1:
#         tagger_component('OpenSearch', [health, version])
#     with col2:
#         st.markdown(opensearch_platform_button, unsafe_allow_html=True)

#     if 'tenant_id' in st.session_state:
#         platform_admin()
    
#     if 'tenant_id' not in st.session_state:
#         st.text('Please Sign In')




 