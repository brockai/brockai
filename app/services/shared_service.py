import streamlit as st

from datetime import datetime
from helpers.config import client
from services.s3api import upload_files
from helpers.config import platform_admin_tenant

def check_opensearch_health():
    try:
        info = client.info()
        if info:
            return f"Cluster 👍", "Version "+info['version']['number']
        else:
            platform_log('error', 'check_opensearch_health failed', 'shared_service', platform_admin_tenant)
            return f"Cluster 👎", "Version ❌"

    except Exception as e:
        platform_log('error', 'check_opensearch_health failed', 'shared_service', platform_admin_tenant)
        return f"Cluster Down! 👎", "Version ❌"

def is_index(tenant_id, index):
    try:
        response = client.indices.exists(index)
        return response

    except Exception as e:
        platform_log('error', 'check_opensearch_health failed', 'shared_service', tenant_id)
        return e

def s3_tenant_files(files):        
    for file in files:
        file_name=file.name
        bytes_data = file.getvalue()
        upload_files(bytes_data, file_name)
                            
        st.session_state["file_uploader_key"] += 1
                       
    return


def platform_log(type, message, service, tenant_id):

    data = {
        "type": type,
        "message": message,
        "service": service,
        "tenant_id": tenant_id,
        "datetime": datetime.now()
    }

    try:
        response = post_platform_doc(tenant_id, 'platform_logs', data)
        return response

    except Exception as e:
        error_message = str(e)
        platform_log('error','platform logs failed: '+error_message, 'shared_service', tenant_id)
        return e

def post_platform_doc(tenant_id, index, data): 

    request_body = {
        **data
    }

    try:
        response = client.index(index, body=request_body, ignore=400)
        return response

    except Exception as e:
        error_message = str(e)
        if 'tenant_id' in st.session_state:
            tenant_id = st.session_state['tenant_id']    
            platform_log('error','post platform doc failed: '+error_message, 'shared_service', tenant_id)

        return e