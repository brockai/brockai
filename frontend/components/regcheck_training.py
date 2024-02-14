def regcheck_training():
    import base64
    import streamlit as st
    import pandas as pd
    import streamlit_antd_components as sac
    
    from datetime import datetime
    from services.tenant_service import post_tenant_files, get_tenant_files
    from components.platform_auth import signin_button
    from helpers.antd_utils import show_space

    st.markdown(
        f'<style>.df .col-Name {{max-width: 100%;}}</style>', 
        unsafe_allow_html=True
    )

    tenant_files = get_tenant_files()
    if tenant_files:
                    
        if len(tenant_files['hits']['hits']) > 0:
            file_name_list = []

            col1, col2 = st.columns([3,5])

            for hit in tenant_files['hits']['hits']:
                obj = hit['_source']['file_name']
                    
                file_name_list.append(obj)

                st.session_state['tenant_file_names'] = file_name_list

            with col1: 
                st.selectbox('Select Dataset', file_name_list)
            with col2:
                st.text_input('Search Dataset')
