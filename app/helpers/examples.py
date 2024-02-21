import streamlit as st
import subprocess

def run_search():
    try:
        subprocess.run(["python", "examples/deepset/search.py"], check=True)
    except subprocess.CalledProcessError as e:
        st.error(f"Error: {e}")
    else:
        st.success("Sucess")
        
def run_fileupload():
    try:
        subprocess.run(["python", "examples/deepset/fileupload.py"], check=True)
    except subprocess.CalledProcessError as e:
        st.error(f"Error: {e}")
    else:
        st.success("Success")