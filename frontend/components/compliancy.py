def compliancy():
    import base64
    import streamlit as st
    import pandas as pd
    import streamlit_antd_components as sac
    
    from datetime import datetime
    from services.opensearch import post_document
    from components.auth import signin_button
    from helpers.antd_utils import show_space

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

    if "current_step_index" not in st.session_state:
        st.session_state['current_step_index'] = 0 

    if 'docs' in st.session_state:
        hit_count = st.session_state['docs']['hits']['total']['value']
    else:
        hit_count = 0

    filecount = sac.Tag(hit_count, color='red', bordered=False)
    tab = sac.tabs([
        sac.TabsItem(label='Reg Check', tag=filecount),
        sac.TabsItem(label='Jupyter Notebooks'),
    ], )   

    if not access_token:
        show_space(1)
        signin_button()

    if tab == 'Reg Check':
        show_space(1)
        step = sac.steps(
                items=[
                    sac.StepsItem(title='Step 1', icon='cloud-arrow-up', subtitle='Upload Files', description='File Library, Structured & Unstructured data'),
                    sac.StepsItem(title='Step 2', icon='arrow-clockwise', subtitle='Processing', description='Data Extraction, Classification, Compliancy Check, AI-driven Risk Assessment'),
                    sac.StepsItem(title='Step 3', icon='shield-check', subtitle='Regulatory Management', description='AI-driven Similar Files Lookup, Continous Feedback Loop & Model Trianing, Real-time Data & Reports'),
                ], index=st.session_state['current_step_index']
            )

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

                            mappings = {
                                'name': file.name,
                                'metadata': {
                                    'created_date': datetime.now(),
                                    'file_size': file.size,
                                    'data_extraction': 'Not Started',
                                    'classification': 'Not Started',
                                    'compliancy_check': 'Not Started',
                                    'risk_assessment': 'Not Started',
                                    'similar_files': 'Not Started'
                                },
                                'file': {
                                    'content': base64_data
                                }
                            }

                            st.session_state["file_uploader_key"] += 1
                                    
                            post_document(mappings)
                        st.session_state['current_step_index'] = 1
                        st.rerun()

        if step == 'Step 2':
            st.markdown(
                f'<style>.df .col-Name {{max-width: 100%;}}</style>', 
                unsafe_allow_html=True
            )
            if access_token:
                processing = sac.Tag('Processing', color='blue', bordered=False)
                get_step('Step 2', 'arrow-clockwise', processing)
                
                hits = st.session_state['tenant_files']['hits']

                if len(hits) > 0:
                    file_list = []
                    for hit in hits:
                        obj = {
                            'File Name': hit['_source']['name'],
                            'File Size': hit['_source']['metadata']['file_size'],
                            'Data Extracted': hit['_source']['metadata']['data_extraction'],
                            'Data Classified': hit['_source']['metadata']['classification'],
                            'Compliancy Check': hit['_source']['metadata']['compliancy_check'], 
                            'Risk Assessment': hit['_source']['metadata']['risk_assessment'], 
                            'Similar Files': hit['_source']['metadata']['similar_files'], 
                            'Date Created': hit['_source']['metadata']['created_date'],
                        }
                
                        file_list.append(obj)

                    df = pd.DataFrame(file_list)
                    st.write(df)
            
        if step == 'Step 3':
            st.write('got here 3')    