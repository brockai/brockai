def compliancy():
    import requests
    import streamlit as st
    import pandas as pd
    import streamlit_antd_components as sac
    
    from services.s3api import uploadFiles
    from services.opensearch import create_index
    from components.auth import signin_button

    from helpers.antd_utils import show_space

    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0

    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []

    col1, col2, col3 =  st.columns([0.25, 10, 0.25])

    with col2: 
        if st.session_state['access_token'] == '':

            st.write("Full-cycle Bill of Materials (BOM) regulatory check using AI and machine learning to assist in ensuring compliance with regulatory requirements throughout the entire lifecycle of a product.")
            signin_button()

        show_space(1)
        step = sac.steps(
            items=[
                sac.StepsItem(title='step 1', icon='cloud-arrow-up', subtitle='✨ Upload Files', description='File Library, Structured & Unstructured data'),
                sac.StepsItem(title='step 2', icon='arrow-clockwise', subtitle='Processing', description='Data Extraction, Classification, Compliancy Check, AI-driven Risk Assessment'),
                # sac.StepsItem(title='step 3', subtitle='Reports', description='Compliancy & Risk Assessment'),
                sac.StepsItem(title='step 3', icon='shield-check', subtitle='Regulatory Management', description='AI-driven Compliancy Checks, Continous Feedback Loop & Model Trianing, Real-time Data & Reports'),
            ], 
        )

        st.write(step)

        if step == 'step 1':

            # if st.session_state.access_token != '':
            #     getFiles()
            
            files = st.file_uploader(
                "Choose a CSV file", 
                accept_multiple_files=True, 
                type=["txt", "csv"],
                key=st.session_state["file_uploader_key"],
            )

            if files:
                st.session_state["uploaded_files"] = files
                if st.session_state.access_token != '':
                    if st.button('Create Tenant'):
                            create_index()

                    if st.button("🚀 Upload & Process"):
                        for file in files:
                            file_name=file.name
                            bytes_data = file.getvalue()
                            isUpload = uploadFiles(bytes_data, file_name)

                        st.session_state["file_uploader_key"] += 1
                        
                        st.rerun()


        if step == 'step 2':
            st.write('got here 2')

        if step == 'step 3':
            st.write('got here 3')    