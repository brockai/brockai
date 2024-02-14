import streamlit as st
import time
import base64
from datetime import datetime
from services.utils_service import client
from services.mappings import match_all_query, default_index_settings, tenant_index_mappings, files_index_mappings

step1_file_label = ' files sent for Processing...'
    
def get_tenant_doc():
    try:
        response = client.search(body=match_all_query, index=st.session_state.tenant_id, size=10000)
        return response
       
    except Exception as e:
        # left here on purpose, hard error
        st.write(Exception, e)
        return e    
    
def get_tenant_files():
    try:
        response = client.search(body=match_all_query, index=st.session_state.tenant_id+'_files', _source_excludes='file', size=10000)
        return response
       
    except Exception as e:
        # left here on purpose, hard error
        st.write(Exception, e)
        return e    

def post_tenant_files(mappings):

    request_body = {
        **mappings
    }
    
    try:
        response = client.index(st.session_state.tenant_id+'_files', body=request_body, ignore=400)
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
        st.write(response)
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

def opensearch_tenant_files(files):
    
    with st.spinner(text="In progress"):
        for file in files:
            bytes_data = file.getvalue()
                                    
            # byte data encoded for opensearch
            base64_data = base64.b64encode(bytes_data).decode('utf-8')

            mappings = {
                'file_name': file.name,
                'created_date': datetime.now(),
                'file_size': file.size,
                'data_extraction': 'Not Started',
                'classification': 'Not Started',
                'compliancy_check': 'Not Started',
                'risk_assessment': 'Not Started',
                'similar_files': 'Not Started',
                'file': {
                    'content': base64_data
                }
            }

            st.session_state["file_uploader_key"] += 1
                        
            response = post_tenant_files(mappings)
        
    if response['result'] == "created":

        tenant_files = get_tenant_files()
        if tenant_files:
            st.session_state['tenant_files'] = tenant_files['hits']
            st.session_state['file_count'] = str(tenant_files['hits']['total']['value'])
            st.session_state['notification_message'] = '👍 '+ str(len(files)) + step1_file_label
            return True
    else:
        return False
