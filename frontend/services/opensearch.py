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
            return f"Cluster Down! 👎", "Version ❌"

    except Exception as e:
        # left here on purpose, hard error
        st.write(Exception, e)
        return f"Cluster Down! 👎", "Version ❌"

def is_index():
    try:
        response = client.indices.exists(st.session_state.tenant_id)
        return response

    except Exception as e:
        # left here on purpose, hard error
        st.write(Exception, e)
        return e
    
def all_docs():

    query = {
        "query": {
            "match_all": {}
        }
    }

    try:
        return client.search(body=query, index=st.session_state.tenant_id, _source_excludes='file', size=10000)

        # if response.status_code != 404:
        #     return response
        # else:
        #     return {}

    except Exception as e:
        # left here on purpose, hard error
        st.write(Exception, e)
        return e    

def post_document(document): 
    try:
        response = client.index(st.session_state.tenant_id, body=document)
        return response

    except Exception as e:
        # left here on purpose, hard error
        st.write(Exception, e)
        return e

def create_index():
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        }
    }

    index_mappings = {
        'mappings': {
            'properties': {
                'name': {'type': 'text'},
                'metadata': {
                    'properties': {
                        'created_date': {'type': 'date'},
                        'file_size': {'type': 'integer'},
                        'data_extraction': {'type': 'text'},
                        'classification': {'type': 'text'},
                        'compliancy_check': {'type': 'text'},
                        'risk_assessment': {'type': 'text'},
                        'similar_files': {'type': 'text'},
                        'application_redirect':  {'type': 'text'}
                    }
                },
                "file": {
                    "properties": {
                        "content": {
                            "type": "binary"
                        }
                    }
                }
            }
        }
    }

    request_body = {
        **index_settings,
        **index_mappings
    }
    
    try:
        response = client.indices.create(index=st.session_state.tenant_id, body=request_body, ignore=400)
        st.write(response)
        if 'acknowledged' in response and response['acknowledged']:
            print(f"Index '{st.session_state.tenant_id}' created successfully")
        else:
            print(f"Failed to create index '{st.session_state.tenant_id}'")
        return response
    
    except Exception as e:
        st.write(e)
        print(f"Error creating index: {e}")
