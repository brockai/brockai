
import streamlit as st
st.set_page_config(layout="wide")
# import logging
# logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
# logging.getLogger("haystack").setLevel(logging.INFO)

import pandas as pd

from helpers.markdown import sidebar_links_footer, app_header
from helpers.errorcheck import elasticsearch_health

st.title("👑 deepset File Upload & Search 🧪")

with open('styles.css') as f:
    st.sidebar.markdown(
        f'<style>{f.read()}</style>'
        +app_header
        +sidebar_links_footer
        , unsafe_allow_html=True
    )
from deepset.piplines import deepset_indexsearch
pipelineIndex = deepset_indexsearch()

isHealthy = elasticsearch_health()

# if isHealthy:
#     from helpers.piplines import deepset_indexsearch
#     pipelineIndex = deepset_indexsearch()
# else:
#     st.error(':disappointed: Sorry, the system is not available right now')    
    
uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True, disabled=not isHealthy)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    # st.write(bytes_data)
      
question = st.text_input(
    "Search for compliancy by part no, supplier, manufacturer and more", 
    placeholder="Enter part no, supplier, manufacturer",
    max_chars=100, disabled=not uploaded_files)

run_pressed = st.button("Run", disabled=not uploaded_files)

if run_pressed and isHealthy:
    from deepset.piplines import deepset_prediction_pipeline
    pipelineQuery = deepset_prediction_pipeline(question)
    answer_df = pd.DataFrame(pipelineQuery["answers"])
    answer_df

