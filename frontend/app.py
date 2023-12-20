import streamlit as st

from st_pages import show_pages_from_config 
st.set_page_config(layout="wide", page_title="brockai - Platform", page_icon="./static/brockai.png")  
show_pages_from_config()

import re
from openai import OpenAI

from helpers.config import openaikey
from helpers.markdown import sidebar_footer_logo, sidebar_app_header, powered_by_openai, platform_link

client = OpenAI(api_key=openaikey)   

if "messages_bot" not in st.session_state:
    st.session_state["messages_bot"] = [{"role": "assistant", "content": "Would you like to learn more about adding AI to your app?"}]
    
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
           
with open('styles.css') as f:
    st.sidebar.markdown(
        f'<style>{f.read()}</style>'
        +sidebar_app_header
        +sidebar_footer_logo
        , unsafe_allow_html=True
    )

st.sidebar.markdown(platform_link, unsafe_allow_html=True)
# st.markdown("[Click here to visit OpenAI's website](https://openai.com)")

st.header("🕵️‍♀️ Blaire")

st.markdown(powered_by_openai, unsafe_allow_html=True)

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

   