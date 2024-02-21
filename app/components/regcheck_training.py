def regcheck_training():
    import base64
    import streamlit as st
    import pandas as pd
    from io import StringIO
    import streamlit_antd_components as sac
    
    from datetime import datetime
    from services.tenant_service import get_tenant_files, get_tenant_file
    from components.platform_auth import signin_button
    from helpers.antd_utils import show_space

    st.markdown(
        f'<style>.df .col-Name {{max-width: 100%;}}</style>', 
        unsafe_allow_html=True
    )

    tenant_files = get_tenant_files(st.session_state['tenant_id'])
    if tenant_files:
                    
        if len(tenant_files['hits']['hits']) > 0:
            file_list = {}

            col1, col2 = st.columns([3,5])

            for hit in tenant_files['hits']['hits']:
                file_list[hit['_id']] = hit['_source']['file_name']

            with col1:
                selected_dataset = st.selectbox('Select Dataset', file_list.keys(), format_func=lambda x:file_list[ x ])
            with col2:
                st.text_input('Search Dataset')

    file = get_tenant_file(st.session_state['tenant_id'], selected_dataset)

    binary_data = file['hits']['hits'][0]['_source']['file']['content']
    decoded_text = base64.b64decode(binary_data).decode('utf-8')

    df = pd.read_csv(StringIO(decoded_text))
    st.write(df)