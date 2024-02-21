import streamlit as st

from services.utils_service import client

from services.mappings import match_all_query, default_index_settings, tenant_index_mappings, files_index_mappings

def get_tenant_dataset():
    try:
        response = client.search(body=match_all_query, index=st.session_state.tenant_id, _source_excludes='file', size=10000)
        return response
       
    except Exception as e:
        # left here on purpose, hard error
        st.write(Exception, e)
        return e    

