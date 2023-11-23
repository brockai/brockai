import streamlit as st
from st_pages import show_pages_from_config

import os
from openai import OpenAI
st.set_page_config(layout="wide") 

from utils.ui import set_initial_state

from helpers.markdown import sidebar_footer_logo, app_header

show_pages_from_config()

set_initial_state()

with open('styles.css') as f:
    st.sidebar.markdown(
        f'<style>{f.read()}</style>'
        +app_header
        +sidebar_footer_logo
        , unsafe_allow_html=True
    )
    
    # url =  "http://127.0.0.1:8000/docs"
    # link = f'<a href="{url}" target="_blank">{url}</a>'
    # st.sidebar.markdown(link, unsafe_allow_html=True)
        
st.title("🕵 AI Bussiness Analyst")
st.caption("🚀 Powered by OpenAI LLM")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi I'm Blaire, please tell me about your use case?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not os.getenv("OPENAI_KEY"):
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
