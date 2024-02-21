import streamlit as st
from datetime import datetime
from helpers.config import client

from services.mappings import match_all_query, models, default_index_settings, platform_index_mappings, admin_role, pipelines, platform_log_mappings

def platform_log(type, message, service, tenant_id):

    data = {
        "mappings": {
            "properties": {
                "type": type,
                "message": message,
                "service": service,
                "tenant_id": tenant_id,
                "datetime": datetime.now()
            }
        }
    }

    try:
        response = post_platform_doc(tenant_id, 'platform_logs', data)
        return response

    except Exception as e:
        error_message = str(e)
        platform_log('error','platform logs failed: '+error_message, 'platform_service', tenant_id)
        return e
    
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
            platform_log('error','put platform doc failed: '+error_message, 'platform_service', tenant_id)

        return e

def post_platform_doc(tenant_id, index, data): 

    request_body = {
        **data
    }

    try:
        response = client.index(index , body=request_body, ignore=400)
        return response

    except Exception as e:
        error_message = str(e)
        if 'tenant_id' in st.session_state:
            tenant_id = st.session_state['tenant_id']    
            platform_log('error','post platform doc failed: '+error_message, 'platform_service', tenant_id)

        return e
    
def platform_nlp_ingest(tenant_id):
        
    try:
        response = client.indices.get(index='platform-nlp-ingest')
        return response
       
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'platform nlp ingest failed: '+error_message, 'platform_service', tenant_id)
        return e   
    
def is_tenant_platform_settings(tenant_id):

    field_name = 'tenants'
    search_query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            f"{field_name}.keyword": tenant_id
                        }
                    }
                ]
            }
        }
    }

    try:
        response = client.search(index='platform_settings', body=search_query)

        if response['hits']['total']['value'] > 0:
            return True
        else:
            return False
        
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'is tenant platform settings failed: '+error_message, 'platform_service', tenant_id)
        return e

def add_tenant_platform_settings(tenant_id):

    app_tenant = {"index": tenant_id}

    # Define the update query
    update_query = {
        "script": {
            "source": f"ctx._source['tenants'].add(params.newObject)",
            "lang": "painless",
            "params": {
                "newObject": app_tenant
            }
        },
        "query": {
            "match_all": {}
        }
    }

    try:
        response = client.update_by_query(index='platform_settings', body=update_query)
        return response
    
    except Exception as e:
        error_message = str(e)
        if not "400" in error_message:
            platform_log('error', 'add tenant platform settings failed: '+error_message, 'platform_service', tenant_id)
        
        return e
    
def get_logs(tenant_id):

    try:
        response = client.search(body=match_all_query, index='platform_logs')
        return response
       
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'get logs failed :'+error_message, 'tenant_service', tenant_id)
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

    request_body = {
        **default_index_settings,
        **platform_index_mappings
    }
    
    try:
        response = client.indices.create(index='platform_settings' , body=request_body, ignore=400)
        
        if 'acknowledged' in response and response['acknowledged']:
        
            tenants = {"tenants":[{"index":tenant_id}]}
            
            data = {
                "mappings": {
                    "properties": {
                        "name": 'Platform Settings',
                        "roles": admin_role,
                        "pipelines": pipelines,
                        "models": models,
                        "tenants": tenants
                    }
                }
            }
            
            try:
                response = post_platform_doc(tenant_id, 'platform_settings', data)

                if response:
                    platform_log('acknowledged', 'create platform settings succeeded: '+response, 'tenant_service', tenant_id)

            except Exception as e:
                error_message = str(e)
                platform_log('error', 'platform settings document failed :'+error_message, 'platform_service', tenant_id)
                return e
            
        elif response['error']['root_cause']['type'] != 'resource_already_exists_exception':
            error_message = str(e)
            platform_log('error', 'platform settings document failed: '+error_message, 'platform_service', tenant_id)
            return e
        
        return response
    
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'platform settings failed:'+error_message, 'platform_service', tenant_id)
        return e 

def create_platform_logs(tenant_id):

    request_body = {
        **default_index_settings,
        **platform_log_mappings
    }
    
    try:
        response = client.indices.create(index='platform_logs' , body=request_body, ignore=400)
        
        if 'acknowledged' in response and response['acknowledged']:
            
            data = {
                "mappings": {
                    "properties": {
                        "type": 'acknowledged',
                        "message": 'platform_logs created',
                        "service": 'platform_service',
                        "tenant_id": tenant_id,
                        "datetime": datetime.now()
                    }
                }
            }
            
            try:
                response = post_platform_doc('platform logs', data)

                if response:
                    platform_log('acknowledged', 'create platform logs succeeded: '+response, 'tenant_service', tenant_id)

            except Exception as e:
                error_message = str(e)
                platform_log('error', 'platform logs entry failed: '+error_message, 'platform_service', tenant_id)
                return e 
            
        elif response['error']['root_cause']['type'] != 'resource_already_exists_exception':
            platform_log('create platform logs failed', 'platform_service', tenant_id)
        
        return response
    
    except Exception as e:
        error_message = str(e)
        platform_log('error', 'platform logs failed: '+error_message, 'platform_service', tenant_id)
        return e 