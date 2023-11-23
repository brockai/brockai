
import streamlit as st
st.set_page_config(layout="wide")
import logging
logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)

import pandas as pd
from st_keyup import st_keyup

from helpers.piplines import cache_opensearch, prediction_pipeline
from helpers.markdown import sidebar_footer_logo, app_header

st.title("💯 BOM Component Compliancy 🧪")

with open('styles.css') as f:
    st.sidebar.markdown(
        f'<style>{f.read()}</style>'
        +app_header
        +sidebar_footer_logo
        , unsafe_allow_html=True
    )
    
# with tab1:
uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    # st.write(bytes_data)
      
question = st.text_input(
    "Search for compliancy by part no, supplier, manufacturer and more", 
    placeholder="Enter part no, supplier, manufacturer",
    max_chars=100, disabled=not uploaded_files)
print(question)
run_pressed = st.button("Run", disabled=not uploaded_files)

pipelineIndex = cache_opensearch()

if run_pressed:
    pipelineQuery = prediction_pipeline(question)
    answer_df = pd.DataFrame(pipelineQuery["answers"])
    answer_df

