import argparse
import os
from dotenv import load_dotenv

load_dotenv()
parser = argparse.ArgumentParser(description='Generative/Extractive model search with sentence-transformers/all-MiniLM-L12-v2 embeddings')

document_store_choices = ('In Memory', 'Elastic Search', 'Open Search')
task_choices = ('extractive', 'rag')
parser.add_argument('--store', choices=document_store_choices, default='In Memory', help='DocumentStore selection (default: %(default)s)')
parser.add_argument('--task', choices=task_choices, default='rag', help='Task selection (default: %(default)s)')

model_configs = {
    'EMBEDDING_MODEL': os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L12-v2"),
    'GENERATIVE_MODEL': os.getenv("GENERATIVE_MODEL", "gpt-4"),
    'EXTRACTIVE_MODEL': os.getenv("EXTRACTIVE_MODEL", "deepset/roberta-base-squad2"),
}

model_keys = {
    'OPENAI_KEY': os.getenv("OPENAI_KEY"),
    'COHERE_KEY': os.getenv("COHERE_KEY"),
}

document_store_configs = {

# ElasticSearch Config
'ELASTICSEARCH_HOST': os.getenv("ELASTICSEARCH_HOST", "localhost"),
'ELASTICSEARCH_PORT': os.getenv("ELASTICSEARCH_PORT", 9200),

# OpenSearch Config
'OPENSEARCH_SCHEME': os.getenv("OPENSEARCH_SCHEME",  "https"),
'OPENSEARCH_USERNAME': os.getenv("OPENSEARCH_USERNAME", "admin"), 
'OPENSEARCH_PASSWORD': os.getenv("OPENSEARCH_PASSWORD", "admin"),
'OPENSEARCH_HOST': os.getenv("OPENSEARCH_HOST", "localhost"),
'OPENSEARCH_PORT': os.getenv("OPENSEARCH_PORT", 9200),
'OPENSEARCH_INDEX':  os.getenv("OPENSEARCH_INDEX", "document"),
'OPENSEARCH_EMBEDDING_DIM': os.getenv("OPENSEARCH_EMBEDDING_DIM", 768),

# Milvus Config
'MILVUS_URI': os.getenv("MILVUS_URI", "http://localhost:19530/default"),
'MILVUS_INDEX':  os.getenv("MILVUS_INDEX", "document"),
'MILVUS_EMBEDDING_DIM': os.getenv("MILVUS_EMBEDDING_DIM", 768),
}