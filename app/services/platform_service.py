import streamlit as st
import base64
from datetime import datetime
from helpers.config import client
from services.shared_service import platform_log, post_platform_doc

from services.mappings import match_all_query, models, default_index_settings, admin_role, pipelines, files_mappings, logs_mappings, match_tenant_files_query
    
def put_platform_doc(index, doc_id, data): 

    request_body = {
        **data
    }

    try:
        response = client.index(index=index, body=request_body, id=doc_id, ignore=400)
        return response

    except Exception as e:
        error_message = str(e)
        if 'tenant_id' in st.session_state:
            tenant_id = st.session_state['tenant_id']    
            platform_log('error', 'put platform doc failed: '+error_message, 'platform_service', tenant_id)

        return e
    
def platform_nlp_ingest(tenant_id):
        
    try:
        response = client.indices.get(index='platform-nlp-ingest')
        return response
       
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'platform nlp ingest failed: '+error_message, 'platform_service', tenant_id)
        return e   
 
    
def get_logs(tenant_id):

    try:
        response = client.search(body=match_all_query, index='platform_logs')
        return response
       
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'get logs failed :'+error_message, 'platform_service', tenant_id)
        return e
    
def get_platform_tenants(tenant_id):

    try:
        index_pattern = 'platform*'

        response = client.cat.indices(index=index_pattern, format='json')

        tenants = []
        remove_prefex = "platform_"
        indices_to_exclude = ["settings", "logs", "files", "ingest"]
        
        for tenant in response:
            contains_index = any(idx in tenant['index'] for idx in indices_to_exclude)
            if not contains_index:
                index = tenant['index'][len(remove_prefex):]
                tenants.append(index)

        return tenants
       
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'get logs failed :'+error_message, 'platform_service', tenant_id)
        return e    

def get_platform_settings(tenant_id):
     
    try:
        response = client.search(body=match_all_query, index='platform_settings', size=10000)
        return response
       
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'get platform settings failed: '+error_message, 'platform_service',  tenant_id)
        return e

def create_platform_settings(tenant_id):

    data = {
        "name": 'Platform Settings',
        "roles": admin_role,
        "pipelines": pipelines,
        "models": models
    }
            
    try:
        response = post_platform_doc(tenant_id, 'platform_settings', data)
        
        if response['result'] == 'created':
            platform_log('created', 'create platform settings succeeded', 'platform_service', tenant_id)

    except Exception as e:
        error_message = str(e)
        platform_log('error', 'create platform settings failed:'+error_message, 'platform_service', tenant_id)
        return e 

def create_platform_tenant(tenant_id, user_info, roles):

    data = {
        "name": user_info["name"],
        "given_name": user_info["given_name"],
        "email": user_info["email"],
        "roles": roles
    }

    try:
        response = post_platform_doc(tenant_id, 'platform_'+tenant_id, data)

        if response['result'] == 'created':
            platform_log('created', 'create tenant succeeded', 'platform_service', tenant_id)

    except Exception as e:
        error_message = str(e)
        platform_log('error', 'post tenant document failed:'+error_message, 'platform_service', tenant_id)
        return e

def create_platform_logs(tenant_id):

    request_body = {
        **default_index_settings,
        **logs_mappings
    }
            
    try:
        response = client.indices.create(index='platform_logs', body=request_body, ignore=400)

        if response['acknowledged']:
            platform_log('created', 'create platform logs succeeded', 'platform_service', tenant_id)

        return response

    except Exception as e:
        error_message = str(e)
        platform_log('error', 'create platform logs failed: '+error_message, 'platform_service', tenant_id)
        return e     

def create_tenant_files(tenant_id):

    request_body = {
        **default_index_settings,
        **files_mappings
    }
    
    try:
        response = client.indices.create(index='platform_'+tenant_id+'_files', body=request_body, ignore=400)
        
        if response['acknowledged']:
            platform_log(f'created', 'create tenant files succeeded', 'platform_service', tenant_id)

        return response
    
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'create tenant files failed:'+error_message, 'platform_service', tenant_id)
        return e

def get_platform_files(tenant_id):
     
    try:
        response = client.search(body=match_tenant_files_query, index='platform_'+tenant_id+'_files', size=100)
        return response
       
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'get platform settings failed: '+error_message, 'platform_service',  tenant_id)
        return e