import streamlit as st

from opensearchpy import OpenSearch
from helpers.config import opensearch_user, opensearch_password, opensearch_host, opensearch_host_port
from services.s3api import upload_files

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
        return response

    except Exception as e:
        # left here on purpose, hard error
        st.write(Exception, e)
        return e

def s3_tenant_files(files):        
    for file in files:
        file_name=file.name
        bytes_data = file.getvalue()
        upload_files(bytes_data, file_name)
                            
        st.session_state["file_uploader_key"] += 1
                       
    return