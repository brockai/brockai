import streamlit as st

import os
from haystack import Pipeline

doc_dir = "../data"

from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import TextConverter, PreProcessor, FARMReader, BM25Retriever

document_store = ElasticsearchDocumentStore(host="localhost", port="9201", index="bom123")
    
@st.cache_resource(show_spinner=False)
def deepset_indexsearch():
    indexing_pipeline = Pipeline()
    text_converter = TextConverter()
    preprocessor = PreProcessor(
      clean_whitespace=True,
      clean_header_footer=True,
      clean_empty_lines=True,
      split_by="word",
      split_length=200,
      split_overlap=20,
      split_respect_sentence_boundary=True,
    )

    indexing_pipeline.add_node(component=text_converter, name="TextConverter", inputs=["File"])
    indexing_pipeline.add_node(component=preprocessor, name="PreProcessor", inputs=["TextConverter"])
    indexing_pipeline.add_node(component=document_store, name="DocumentStore", inputs=["PreProcessor"])
    
    files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
    indexing_pipeline.run_batch(file_paths=files_to_index)
    
    return indexing_pipeline

@st.cache_resource(show_spinner=True)
def deepset_prediction_pipeline(question):
    query_pipeline = Pipeline()
    retriever = BM25Retriever(document_store=document_store)
    reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

    query_pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
    query_pipeline.add_node(component=reader, name="Reader", inputs=["Retriever"])

    prediction = query_pipeline.run(
        query = question, params={"Retriever": {"top_k": 10}, "Reader": {"top_k": 3}}
    )
    
    from pprint import pprint
    pprint(prediction["answers"])

    return prediction

@st.cache_data(show_spinner=True)
def query(_pipeline, question):
    params = {}
    results = _pipeline.run(question, params=params)
    return results