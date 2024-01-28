import streamlit as st
import requests
from opensearchpy import OpenSearch
from helpers.config import opensearch_user, opensearch_password, opensearch_host, opensearch_host_port

auth = (opensearch_user, opensearch_password)

client = OpenSearch(
    hosts = [{'host':  opensearch_host, 'port': opensearch_host_port}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = False
)

def check_opensearch_health():
    
    try:
        info = client.info()
        
        if info:
            return f"Cluster Up! 👍", "Version "+info['version']['number']
        else:
            return f"Cluster Down! 👎"

    except requests.RequestException as e:
        return f"Cluster Down! 👎"

def create_index():
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        }
    }

    index_mappings = {
        "mappings": {
            "properties": {
                "field1": {"type": "keyword"},
                "field2": {"type": "text"}
                # Add more field definitions as needed
            }
        }
    }
    
    try:
        response = client.indices.create(index=st.session_state.tenant_id, body=index_settings, ignore=400)
        st.write(response)
        if 'acknowledged' in response and response['acknowledged']:
            print(f"Index '{st.session_state.tenant_id}' created successfully")
        else:
            print(f"Failed to create index '{st.session_state.tenant_id}'")

    except Exception as e:
        print(f"Error creating index: {e}")
