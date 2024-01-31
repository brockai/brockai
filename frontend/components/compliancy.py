def compliancy():
    import requests
    import streamlit as st
    import pandas as pd
    from datetime import datetime
    import streamlit_antd_components as sac
    
    from services.s3api import upload_files
    from services.opensearch import post_document, all_docs
    from components.auth import signin_button
    
    from helpers.antd_utils import show_space

    import base64

    access_token = st.session_state.get("access_token")
    
    disable_fileup_loader = True
    if access_token:
        disable_fileup_loader = False

    def get_step(title, icon, tag):
        title = sac.menu(
            items=[
                sac.MenuItem(title, icon=icon, tag=tag)
                ],
                key=title,
                open_all=True, indent=20,
                format_func='title'
        )
        return title

    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0

    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []

    if not access_token:
        st.write("Full-cycle Bill of Materials (BOM) regulatory check using AI and machine learning to assist in ensuring compliance with regulatory requirements throughout the entire lifecycle of a product.")
    else:
        show_space(1)

    if "current_step_index" not in st.session_state:
        st.session_state['current_step_index'] = 0    

    step = sac.steps(
        items=[
            sac.StepsItem(title='Step 1', icon='cloud-arrow-up', subtitle='Upload Files', description='File Library, Structured & Unstructured data'),
            sac.StepsItem(title='Step 2', icon='arrow-clockwise', subtitle='Processing', description='Data Extraction, Classification, Compliancy Check, AI-driven Risk Assessment'),
            # sac.StepsItem(title='step 3', subtitle='Reports', description='Compliancy & Risk Assessment'),
            sac.StepsItem(title='Step 3', icon='shield-check', subtitle='Regulatory Management', description='AI-driven Similar Files Lookup, Continous Feedback Loop & Model Trianing, Real-time Data & Reports'),
        ], index=st.session_state['current_step_index']
    )

    if not access_token:
        show_space(1)
        signin_button()

    if step == 'Step 1':

        if access_token:
            upload = sac.Tag('Upload Files', color='blue', bordered=False)
            get_step('Step 1', 'cloud-arrow-up', upload)
            st.session_state['current_step_index'] = 0
            
        files = st.file_uploader(
            "Choose a CSV file", 
            accept_multiple_files=True, 
            type=["txt", "csv"],
            key=st.session_state["file_uploader_key"],
            disabled=disable_fileup_loader
        )

        if files:
            st.session_state["uploaded_files"] = files
            if access_token:
                if st.button("🚀 Upload & Process"):
                    for file in files:
                        # left here on purpose, example of writing file to s3
                        # st.write(file)
                        # file_name=file.name
                        # bytes_data = file.getvalue()
                        # upload_files(bytes_data, file_name)
                       
                        bytes_data = file.getvalue()
                        
                        # byte data encoded for opensearch
                        base64_data = base64.b64encode(bytes_data).decode('utf-8')
                        document = {
                            'name': file.name,
                            'metadata': {
                                'created_date': datetime.now(),
                                'file_size': file.size,
                                'data_extraction': 'Not Started',
                                'classification': 'Not Started',
                                'compliancy_check': 'Not Started',
                                'risk_assessment': 'Not Started',
                                'similar_files': 'Not Started',
                                'application_redirect': 'compliancy'
                            },
                            'file': {
                                'content': base64_data
                            }
                        }

                        st.session_state["file_uploader_key"] += 1
                                
                    post_document(document)

                    st.session_state['current_step_index'] = 1
                    st.rerun()


    if step == 'Step 2':
        if access_token:
            processing = sac.Tag('Processing', color='blue', bordered=False)
            get_step('Step 2', 'arrow-clockwise', processing)
            # response = all_docs()
            # st.write(response)

        

    if step == 'Step 3':
        st.write('got here 3')    