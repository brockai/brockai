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

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if re.match(pattern, email):
        return True
    else:
        return False

def generate_captcha():
    captcha_text = "".join(random.choices(mailgun['options'], k=6))
    image = ImageCaptcha(width=400, height=100).generate(captcha_text)
    return captcha_text, image
  
with open('styles.css') as f:
    st.sidebar.markdown(
        f'<style>{f.read()}</style>'
        +sidebar_app_header
        +sidebar_footer_logo
        , unsafe_allow_html=True
    )
    
st.sidebar.link_button(":abacus: Platform Signin", scheme+domain_platform, use_container_width=True)

st.header("🕵 AI Assistant")

st.markdown(powered_by_openai, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi I'm Blaire, please tell me about your use case?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openaikey:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(openaikey)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

