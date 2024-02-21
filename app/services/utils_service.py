import streamlit as st

# from opensearchpy import OpenSearch
from helpers.config import client
from services.s3api import upload_files
from services.platform_service import platform_log
from helpers.config import platform_admin_tenant

def check_opensearch_health():
    try:
        info = client.info()
        if info:
            return f"Cluster Up! 👍", "Version "+info['version']['number']
        else:
            platform_log('error', 'check_opensearch_health failed', 'utils_service', platform_admin_tenant)
            return f"Cluster Down! 👎", "Version ❌"

    except Exception as e:
        platform_log('error', 'check_opensearch_health failed', 'utils_service', platform_admin_tenant)
        return f"Cluster Down! 👎", "Version ❌"

def is_index(tenant_id, index):
    try:
        response = client.indices.exists(index)
        return response

    except Exception as e:
        platform_log('error', 'check_opensearch_health failed', 'utils_service', tenant_id)
        return e

def s3_tenant_files(files):        
    for file in files:
        file_name=file.name
        bytes_data = file.getvalue()
        upload_files(bytes_data, file_name)
                            
        st.session_state["file_uploader_key"] += 1
                       
    return
