import streamlit as st

from config import document_store_configs, model_configs, model_keys
from haystack import Pipeline
from haystack.schema import Answer
from haystack.document_stores import BaseDocumentStore
from haystack.document_stores import InMemoryDocumentStore, OpenSearchDocumentStore, ElasticsearchDocumentStore

@st.cache_resource(show_spinner=False)
def start_document_store(type: str):
    #This function starts the documents store of your choice based on your command line preference
    if type == 'In Memory':
        document_store = InMemoryDocumentStore(use_bm25=True)
    elif type == 'Open Search':
        document_store = OpenSearchDocumentStore(scheme = document_store_configs['OPENSEARCH_SCHEME'], 
                                                 username = document_store_configs['OPENSEARCH_USERNAME'], 
                                                 password = document_store_configs['OPENSEARCH_PASSWORD'],
                                                 host = document_store_configs['OPENSEARCH_HOST'],
                                                 port = document_store_configs['OPENSEARCH_PORT'],
                                                 index = document_store_configs['OPENSEARCH_INDEX'],
                                                 embedding_dim = document_store_configs['OPENSEARCH_EMBEDDING_DIM'])
    elif type == 'Elastic Search':
        document_store = ElasticsearchDocumentStore(host = document_store_configs['ELASTICSEARCH_HOST'],
                                                    port = document_store_configs['ELASTICSEARCH_PORT'])
                                              
    return document_store
  
@st.cache_resource(show_spinner=False)
def start_all_document_stores():
    #This function starts the documents store of your choice based on your command line preference
    document_store_in_memory = InMemoryDocumentStore(use_bm25=True)
    document_store_open_search = OpenSearchDocumentStore(scheme = document_store_configs['OPENSEARCH_SCHEME'], 
                                                        username = document_store_configs['OPENSEARCH_USERNAME'], 
                                                        password = document_store_configs['OPENSEARCH_PASSWORD'],
                                                        host = document_store_configs['OPENSEARCH_HOST'],
                                                        port = document_store_configs['OPENSEARCH_PORT'],
                                                        index = document_store_configs['OPENSEARCH_INDEX'],
                                                        embedding_dim = document_store_configs['OPENSEARCH_EMBEDDING_DIM'])
    document_store_elastic_search = ElasticsearchDocumentStore(host = document_store_configs['ELASTICSEARCH_HOST'],
                                                              port = document_store_configs['ELASTICSEARCH_PORT'])
                                              
    return document_store_in_memory, document_store_open_search, document_store_elastic_search

# cached to make index and models load only at start
@st.cache_resource(show_spinner=False)
def start_haystack_extractive(_document_store: BaseDocumentStore):
    from haystack.nodes import EmbeddingRetriever, FARMReader
    
    retriever = EmbeddingRetriever(document_store=_document_store, 
                                   embedding_model=model_configs['EMBEDDING_MODEL'], 
                                   top_k=5)
    
    reader = FARMReader(model_name_or_path=model_configs['EXTRACTIVE_MODEL'])
    
    pipe = Pipeline()
    
    pipe.add_node(component=retriever, name="Retriever", inputs=["Query"])
    pipe.add_node(component=reader, name="Reader", inputs=["Retriever"])

    return pipe

@st.cache_resource(show_spinner=False)
def start_haystack_rag(_document_store: BaseDocumentStore):
    from haystack.nodes import EmbeddingRetriever, PromptNode
    
    retriever = EmbeddingRetriever(document_store=_document_store, 
                                   embedding_model=model_configs['EMBEDDING_MODEL'], 
                                   top_k=5)
    
    prompt_node = PromptNode(default_prompt_template="deepset/question-answering", 
                             model_name_or_path=model_configs['GENERATIVE_MODEL'],
                             api_key=model_keys['OPENAI_KEY'])
    pipe = Pipeline()

    pipe.add_node(component=retriever, name="Retriever", inputs=["Query"])
    pipe.add_node(component=prompt_node, name="PromptNode", inputs=["Retriever"])

    return pipe

@st.cache_data(show_spinner=True)
def query(_pipeline, question):
    params = {}
    results = _pipeline.run(question, params=params)
    return results