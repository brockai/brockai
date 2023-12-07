import streamlit as st

from st_pages import show_pages_from_config 
st.set_page_config(layout="wide", page_title="brockai - Platform", page_icon="./static/brockai.png")  
show_pages_from_config()

import re
import random
from openai import OpenAI

from helpers.config import domain_platform, scheme, openaikey
from helpers.markdown import sidebar_footer_logo, sidebar_app_header, powered_by_openai

from captcha.image import ImageCaptcha 
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
    
st.sidebar.link_button(":abacus:&nbsp;&nbsp;&nbsp;Platform Signin", scheme+domain_platform, use_container_width=True)

st.header("🤖 brockBot")

st.markdown(powered_by_openai, unsafe_allow_html=True)
print(st.session_state.messages_bot)

for msg in st.session_state.messages_bot:
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

   