import streamlit as st
from config import model_configs

def set_state_if_absent(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

def set_initial_state():
    set_state_if_absent("question", "")
    set_state_if_absent("results", None)
    set_state_if_absent('model', None)
    set_state_if_absent('document_store', 'In Memory')

def reset_results(*args):
    st.session_state.results = None
    
def set_model(key):
    value = model_configs[key]
    st.session_state['model'] = value
    st.session_state['question'] = ""

def set_store(key):
    st.session_state['document_store'] = key
    