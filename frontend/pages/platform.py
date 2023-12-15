import streamlit as st
import streamlit_antd_components as sac

from st_pages import show_pages_from_config 
st.set_page_config(layout="wide", page_title="brockai - Platform", page_icon="./static/brockai.png")  
show_pages_from_config()

import re
from openai import OpenAI

from helpers.config import opensearch_platform, scheme, openaikey
from helpers.markdown import sidebar_footer_logo, sidebar_app_header, powered_by_openai

client = OpenAI(api_key=openaikey)   

if "messages_bot" not in st.session_state:
    st.session_state["messages_bot"] = [{"role": "assistant", "content": "Would you like to learn more about adding AI to your app?"}]
    
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if re.match(pattern, email):
        return True
    else:
        return False
  
with open('styles.css') as f:
    st.sidebar.markdown(
        f'<style>{f.read()}</style>'
        +sidebar_app_header
        +sidebar_footer_logo
        , unsafe_allow_html=True
    )
    
st.markdown(
    """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    """,
    unsafe_allow_html=True
)    
    
st.markdown(
    """
    <style>
    /* Override Streamlit default width to fit Bootstrap container */
    .full-width {
        width: auto !important;
        max-width: 100% !important;
    }
    </style>
    """
, unsafe_allow_html=True)    
    
st.markdown(
    """
    <div class="container-fluid">
        <div class="row justify-content-between"">
            <div class="col-sm-8">
                <div class="row">
                    <div class="col-sm-auto">
                        <h3>🧮&nbsp;&nbsp;Platform@bclayton403</h3>
                    </div>
                </div>
            </div>
            <div class="col-sm-4">
                <div class="row" justify-content-end>
                    <div class="col-sm-auto">
                        <button class="btn btn-dark">🪢&nbsp;&nbsp;API</button>
                    </div>
                    <div class="col-sm-auto">
                        <button class="btn btn-dark">🪢&nbsp;&nbsp;Profile</button>
                    </div>
                    <div class="col-sm-auto">
                        <button class="btn btn-dark">🔒&nbsp;&nbsp;Logout</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
, unsafe_allow_html=True)

# col1, col2, col3, col4 = st.columns([8,2], gap="small")
# col1, col2 = st.columns([10,2], gap="small")
# col1, col2, col3 = st.columns(3, gap="small")

# with col1:
#     st.write("")  # Empty space for alignment
#     st.button("🪢&nbsp;&nbsp;API")

# with col2:
#     st.write("")  # Empty space for alignment
#     st.button("🪢&nbsp;&nbsp;Profile")    

# with col3:
#     st.write("")  # Empty space for alignment
#     st.button("🔒&nbsp;&nbsp;Logout")    

# st.header("🧮&nbsp;&nbsp;Platform@bclayton403")


tab1, tab2, tab3 = st.tabs(["🔔 Notifications", "Dashboards", "Datasets"])

with tab1:
   st.header("Notifications")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab1:
   st.header("Dashboards")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
   st.header("Datasets")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
   
for msg in st.session_state.messages_bot:
    if msg["role"] == 'assistant':
      st.chat_message(msg["role"],avatar="🕵️‍♀️").write(msg["content"])
    else:
      st.chat_message(msg["role"]).write(msg["content"])
    
if prompt := st.chat_input():
    if not openaikey:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    st.session_state.messages_bot.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    response = client.chat.completions.create(model=st.session_state.openai_model, messages=st.session_state.messages_bot)
    msg = response.choices[0].message.content
    
    st.session_state.messages_bot.append({"role": "assistant", "content": msg})
    st.chat_message("assistant",avatar="🤖").write(msg)

   