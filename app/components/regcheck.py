def regcheck():
    import base64
    import time
    import streamlit as st
    import pandas as pd
    import streamlit_antd_components as sac
    
    from datetime import datetime
    from services.tenant_service import post_tenant_files, get_tenant_files
    from services.airflow_service import run_dag

    from components.platform_auth import signin_button
    from components.regcheck_training import regcheck_training
    from components.regcheck_processing import regcheck_processing
    from helpers.antd_utils import show_space

    access_token = st.session_state.get("access_token")
    
    disable_fileup_loader = True

    if access_token:
        disable_fileup_loader = False

    def get_step(title, icon):
        title = sac.menu(
            items=[
                sac.MenuItem(title, icon=icon)
                ],
                key=title,
                open_all=True, indent=20,
                format_func='title'
        )
        return title

    if "file_uploader_key" not in st.session_state:
        st.session_state["file_uploader_key"] = 0
    
    if "is_notification" not in st.session_state:
        st.session_state["is_notification"] = False

    if "is_step_disabled" not in st.session_state:
        st.session_state["is_step_disabled"] = True

    if not access_token:
        st.write("Full-cycle Bill of Materials (BOM) regulatory check using AI and machine learning to assist in ensuring compliance with regulatory requirements throughout the entire lifecycle of a product.")

        st.session_state['file_count'] = '0'
        st.session_state['current_step_index'] = 0

    if not access_token:
        step_1_description = 'File Library, Structured & Unstructured data'
        step_2_description = 'Extraction, Classification, Compliancy Check, Risk Assessment'
        step_3_description = 'Similar Files Lookup, Continous Feedback Loop, Model Trianing, Analytics'
        signin_button()

    if "current_step_index" not in st.session_state:
        st.session_state['current_step_index'] = 0      

    if access_token:
        disable_fileup_loader = False

        step_1_description = None
        step_2_description = None
        step_3_description = None

    st.session_state["is_step_disabled"] = False

    if st.session_state["is_notification"]:
        st.info(st.session_state['notification_message']) 
        time.sleep(3)
        st.session_state["is_notification"] = False
        st.session_state['notification_message'] = None
        st.rerun()
            
    if 'tenant_id' in st.session_state:
        tenant_files = get_tenant_files(st.session_state['tenant_id'])
        if tenant_files:
            st.session_state['tenant_files'] = tenant_files['hits']
            st.session_state['file_count'] = str(tenant_files['hits']['total']['value'])

    show_space(1)
    step = sac.steps(
        items=[
            sac.StepsItem(title='Step 1', icon='cloud-arrow-up', subtitle='Upload Files', description=step_1_description),
            sac.StepsItem(title='Step 2', icon='arrow-clockwise', subtitle='Processing', description=step_2_description, disabled=st.session_state["is_step_disabled"]),
            sac.StepsItem(title='Step 3', icon='shield-check', subtitle='Compliancy', description=step_3_description, disabled=st.session_state["is_step_disabled"]),
        ], index = st.session_state['current_step_index']
    )
        
    if step == 'Step 1':
        get_step('Step 1 - Upload Files', 'cloud-arrow-up')
                
        files = st.file_uploader(
            "Choose a CSV file", 
            accept_multiple_files=True, 
            type=["txt", "csv"],
            key=st.session_state["file_uploader_key"],
            disabled=disable_fileup_loader
        )

        if files:
            if st.button("🚀 Upload & Process"):
                post_tenant_files(st.session_state['tenant_id'], files)
                # set flag for notification banner on rerun
                st.session_state['notification_message'] = 'File uploaded successfully'
                st.session_state["is_notification"] = True
                st.rerun()

    if step == 'Step 2':
        get_step('Step 2 - Processing', 'arrow-clockwise')

        if st.button('run dag'):
            run_dag('test')

        regcheck_processing()
       
    if step == 'Step 3':
        get_step('Step 3 - Compliancy', 'shield-check')
        regcheck_training()