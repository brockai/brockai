import streamlit as st
import requests
import json
from datetime import datetime
from opensearchpy import OpenSearch
from helpers.config import opensearch_user, opensearch_password, opensearch_host, opensearch_host_port
from services.mappings import match_all_query, default_index_settings, tenant_index_mappings, files_index_mappings

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

def is_index(index):
    try:
        response = client.indices.exists(index)
        st.write(response)
        return response

    except Exception as e:
        # left here on purpose, hard error
        st.write(Exception, e)
        return e
    
def tenant_doc():
    try:
        response = client.search(body=match_all_query, index=st.session_state.tenant_id, size=10000)
        return response
       
    except Exception as e:
        # left here on purpose, hard error
        st.write(Exception, e)
        return e    

def tenant_files():
    try:
        response = client.search(body=match_all_query, index=st.session_state.tenant_id+'_files', _source_excludes='file', size=10000)
        return response
       
    except Exception as e:
        # left here on purpose, hard error
        st.write(Exception, e)
        return e    
    
def post_document(mappings): 

    request_body = {
        **mappings
    }

    try:
        response = client.index(st.session_state.tenant_id, body=request_body, ignore=400)
        return response

    except Exception as e:
        # left here on purpose, hard error
        st.write(Exception, e)
        return e

def create_tenant(user_info):

    request_body = {
        **default_index_settings,
        **tenant_index_mappings
    }
    
    try:
    
        response = client.indices.create(index=st.session_state.tenant_id, body=request_body, ignore=400)
         #{'acknowledged': True, 'shards_acknowledged': True, 'index': 'bclayton403'}
        if 'acknowledged' in response and response['acknowledged']:

            #roles & redirects hard coded for now
            roles = {"roles":[{"name":'tenant'}]}
            app_redirects = {"app_redirects":[{"name":'compliancy'}]}
            
            mappings = {
                "mappings": {
                    "properties": {
                        "name": user_info["name"],
                        "given_name": user_info["given_name"],
                        "email": user_info["email"],
                        "app_redirects": app_redirects,
                        "roles":  roles,
                    }
                }
            }
            
            response_doc = post_document(mappings)
            
            print(response_doc)

            print(f"Index '{st.session_state.tenant_id}' created successfully")
        else:
            print(f"Failed to create index '{st.session_state.tenant_id}'")
        return response
    
    except Exception as e:
        st.write(e)
        print(f"Error creating index: {e}")


def create_file_index():

    request_body = {
        **default_index_settings,
        **files_index_mappings
    }
    
    try:
        response = client.indices.create(index=st.session_state.tenant_id+'_files', body=request_body, ignore=400)
        
        if 'acknowledged' in response and response['acknowledged']:
            print(f"Index '{st.session_state.tenant_id}' created successfully")
        else:
            print(f"Failed to create index '{st.session_state.tenant_id}'")
        return response
    
    except Exception as e:
        st.write(e)
        print(f"Error creating index: {e}")

