import streamlit as st

import base64
from datetime import datetime
from helpers.config import client
from services.mappings import match_all_query
from services.shared_service import platform_log

def get_tenant_doc(tenant_id):
    try:
        response = client.search(body=match_all_query, index='platform_'+tenant_id)
        return response
       
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'get tenant doc failed :'+error_message, 'tenant_service', tenant_id)
        return e

def get_tenant_file(tenant_id, doc_id):

    file_query = {
        "query": {
            "ids": {
            "values": [doc_id]
            }
        },
        "size": 10000,
        "timeout": "300s"
    }
    
    try:
        response = client.search(body=file_query, index='platform_'+tenant_id+'_files')
        return response
       
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'get tenant file failed :'+error_message, 'tenant_service', tenant_id)
        return e    
    
def get_tenant_files(tenant_id):
    try:
        response = client.search(body=match_all_query, index='platform_'+tenant_id+'_files', _source_excludes='file', size=10000)
        return response
       
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'get tenant files failed :'+error_message, 'tenant_service', tenant_id)
        return e    

def post_tenant_files(tenant_id, data):

    try:
        response = client.index('platform'+tenant_id+'_files', body=data, ignore=400)
        return response
       
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'post tenant files failed :'+error_message, 'tenant_service', tenant_id)
        return e    
    
def post_document(tenant_id, data): 

    try:
        response = client.index('platform_'+tenant_id, body=data, ignore=400)
        return response

    except Exception as e:
        error_message = str(e)
        platform_log('error', 'post documnet failed :'+error_message, 'tenant_service', tenant_id)
        return e

## starting poimt to post to airflow
# def post_tenant_files(tenant_id, files):
    
#     with st.spinner(text="In progress"):
#         for file in files:
#             bytes_data = file.getvalue()
                                    
#             # byte data encoded for opensearch
#             base64_data = base64.b64encode(bytes_data).decode('utf-8')

#             data = {
#                 'file_name': file.name,
#                 'created_date': datetime.now(),
#                 'file_size': file.size,
#                 'data_extraction': 'Not Started',
#                 'classification': 'Not Started',
#                 'compliancy_check': 'Not Started',
#                 'risk_assessment': 'Not Started',
#                 'similar_files': 'Not Started',
#                 'file': {
#                     'content': base64_data
#                 }
#             }

#             st.session_state["file_uploader_key"] += 1
            
#             try:          
#                 response = post_tenant_files(tenant_id, data)

#                 if response:
#                     platform_log(f'acknowledged', 'post tenant files succeeded', 'platform_service', tenant_id)

#             except Exception as e:
#                 error_message = str(e)
#                 platform_log(f'error', 'create tenant file index failed: '+error_message, 'platform_service', tenant_id)
#                 return e
            
#     if response['result'] == "created":
#         tenant_files = get_tenant_files(st.session_state['tenant_id'])

#         if tenant_files:
#             st.session_state['tenant_files'] = tenant_files['hits']
#             st.session_state['file_count'] = str(tenant_files['hits']['total']['value'])
#             st.session_state['notification_message'] = '👍 '+ str(len(files)) + ' files sent for Processing...'
#             return True
#     else:
#         return False