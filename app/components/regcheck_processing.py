def regcheck_processing():
    import streamlit as st
    import pandas as pd
    
    from services.tenant_service import get_tenant_files

    st.markdown(
        f'<style>.df .col-Name {{max-width: 100%;}}</style>', 
            unsafe_allow_html=True
    )
    
    tenant_files = get_tenant_files(st.session_state['tenant_id'])
    if tenant_files:
                    
        if len(tenant_files['hits']['hits']) > 0:
            file_list = []
            for hit in tenant_files['hits']['hits']:
                obj = {
                    'File Name': hit['_source']['file_name'],
                    'File Size': hit['_source']['file_size'],
                    'Data Extracted': hit['_source']['data_extraction'],
                    'Data Classified': hit['_source']['classification'],
                    'Compliancy Check': hit['_source']['compliancy_check'], 
                    'Risk Assessment': hit['_source']['risk_assessment'], 
                    'Similar Files': hit['_source']['similar_files'], 
                    'Date Created': hit['_source']['created_date'],
                }
                    
                file_list.append(obj)

            st.session_state['tenant_files']['hits'] = file_list
            df = pd.DataFrame(file_list)
            with st.container():
                st.write(df)