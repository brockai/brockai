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

        # print(response)
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
