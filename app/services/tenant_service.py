import streamlit as st

import base64
from datetime import datetime
from helpers.config import platform_admin_tenant
from services.utils_service import client, is_index
from services.mappings import file_query, match_all_query, default_index_settings, tenant_index_mappings, files_index_mappings, tenant_role, admin_role
from services.platform_service import platform_log

def get_tenant_doc(tenant_id):
    try:
        response = client.search(body=match_all_query, index=tenant_id)
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
        response = client.search(body=file_query, index=tenant_id+'_files')

        # print(response)
        return response
       
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'get tenant file failed :'+error_message, 'tenant_service', tenant_id)
        return e    
    
def get_tenant_files(tenant_id):
    try:
        response = client.search(body=match_all_query, index=tenant_id+'_files', _source_excludes='file', size=10000)
        return response
       
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'get tenant files failed :'+error_message, 'tenant_service', tenant_id)
        return e    

def post_tenant_files(tenant_id, mappings):

    request_body = {
        **mappings
    }
    
    try:
        response = client.index(tenant_id+'_files', body=request_body, ignore=400)
        return response
       
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'post tenant files failed :'+error_message, 'tenant_service', tenant_id)
        return e    
    
def post_document(tenant_id, data): 

    request_body = {
        **data
    }

    try:
        response = client.index(tenant_id, body=request_body, ignore=400)
        return response

    except Exception as e:
        error_message = str(e)
        platform_log('error', 'post documnet failed :'+error_message, 'tenant_service', tenant_id)
        return e

def create_tenant(tenant_id, user_info):

    request_body = {
        **default_index_settings
    }

    # check if first (admin) tenant has been created, if so assign tenant role, if not assign admin role
    roles = tenant_role
    if not is_index(platform_admin_tenant, platform_admin_tenant):
        roles = admin_role

    try:
        response = client.indices.create(index=tenant_id, body=request_body, ignore=400)
            
        if 'acknowledged' in response and response['acknowledged']:
            data = {
                "mappings": {
                    "properties": {
                        "name": user_info["name"],
                        "given_name": user_info["given_name"],
                        "email": user_info["email"],
                        "roles": roles
                    }
                }
            }

            try:
                response = post_document(tenant_id, data)

                if response:
                    platform_log('acknowledged', 'create tenant succeeded: '+response, 'tenant_service', tenant_id)

            except Exception as e:
                error_message = str(e)
                platform_log('error', 'create tenant document failed:'+e, 'tenant_service', tenant_id)
                return e

        elif response['error']['root_cause']['type'] != 'resource_already_exists_exception':
            platform_log('error', 'create tenant failed', 'tenant_service', tenant_id)
            return e

        return response
        
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'create tenant failed :'+error_message, 'tenant_service', tenant_id)
    
def create_tenant_file_index(tenant_id):

    request_body = {
        **default_index_settings,
        **files_index_mappings
    }
    
    try:
        response = client.indices.create(index=tenant_id+'_files', body=request_body, ignore=400)
        
        if 'acknowledged' in response and response['acknowledged']:
            platform_log(f'acknowledged', 'create tenant file index succeeded: '+response, 'tenant_service', tenant_id)

        elif response['error']['root_cause']['type'] != 'resource_already_exists_exception':
            platform_log('error', 'create tenant file index failed', 'tenant_service', tenant_id)

        return response
    
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'create tenant file index failed :'+error_message, 'tenant_service', tenant_id)
        return e

def post_tenant_files(tenant_id, files):
    
    with st.spinner(text="In progress"):
        for file in files:
            bytes_data = file.getvalue()
                                    
            # byte data encoded for opensearch
            base64_data = base64.b64encode(bytes_data).decode('utf-8')

            data = {
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
            
            try:          
                response = post_tenant_files(tenant_id, data)

                if response:
                    platform_log(f'acknowledged', 'post tenant files succeeded: '+response, 'tenant_service', tenant_id)

            except Exception as e:
                error_message = str(e)
                platform_log(f'error', 'create tenant file index failed: '+error_message, 'tenant_service', tenant_id)
                return e
        
    if response['result'] == "created":
        tenant_files = get_tenant_files(st.session_state['tenant_id'])

        if tenant_files:
            st.session_state['tenant_files'] = tenant_files['hits']
            st.session_state['file_count'] = str(tenant_files['hits']['total']['value'])
            st.session_state['notification_message'] = '👍 '+ str(len(files)) + ' files sent for Processing...'
            return True
    else:
        return False
