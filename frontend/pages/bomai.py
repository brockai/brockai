
import streamlit as st
import pandas as pd
import tiktoken
st.set_page_config(layout="wide", page_title="brockai - BOM Compliancy", page_icon="./static/brockai.png")  

# import logging
# logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
# logging.getLogger("haystack").setLevel(logging.INFO)

import pandas as pd

from helpers.config import domain_platform, scheme
from helpers.markdown import sidebar_footer_logo, sidebar_app_header, powered_by_openai
from helpers.utils import embedding_model, embedding_encoding, max_tokens, get_embedding, answer_question

st.header("💯 BOM Component Compliancy")
st.markdown(powered_by_openai, unsafe_allow_html=True)

with open('styles.css') as f:
    st.sidebar.markdown(
        f'<style>{f.read()}</style>'
        +sidebar_app_header
        +sidebar_footer_logo
        , unsafe_allow_html=True
    )
    
st.sidebar.link_button(":abacus:&nbsp;&nbsp;&nbsp;Platform Signin", scheme+domain_platform, use_container_width=True)

uploaded_files = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    # st.write(bytes_data)

if st.button("Run", disabled=not uploaded_files):
    
    input_datapath = "data/Reviews.csv"  # to save space, we provide a pre-filtered dataset
    df = pd.read_csv(input_datapath, index_col=0)
    df = df[["Time", "ProductId", "UserId", "Score", "Summary", "Text"]]

    df = df.dropna()

    df["combined"] = (
        "Title: " + df.Summary.str.strip() + "; Content: " + df.Text.str.strip()
    )

    top_n = 1000
    df = df.sort_values("Time").tail(top_n * 2)  # first cut to first 2k entries, assuming less than half will be filtered out
    df.drop("Time", axis=1, inplace=True)

    encoding = tiktoken.get_encoding(embedding_encoding)

    # omit reviews that are too long to embed
    df["n_tokens"] = df.combined.apply(lambda x: len(encoding.encode(x)))
    df = df[df.n_tokens <= max_tokens].tail(top_n)
    len(df)
    
    embedding_model = "text-embedding-ada-002"
    # This may take a few minutes
    df["embedding"] = df.combined.apply(lambda x: get_embedding(x, embedding_model))
    df.to_csv("data/processed/fine_food_reviews_with_embeddings_1k.csv")

    # st.dataframe(df.head(1000))
    
    answer_question(df, question="What is the best price for coffee?", debug=True)
    