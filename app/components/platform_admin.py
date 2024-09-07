def platform_admin():
    import streamlit as st
    import pandas as pd
    
    from streamlit_extras.tags import tagger_component
    from services.platform_service import get_platform_tenants, get_platform_settings, get_logs, put_platform_doc, get_platform_files
    from services.tenant_service import get_tenant_doc
    from helpers.config import platform_admin_tenant 

    st.markdown(
        f'<style>.df .col-Name {{max-width: 100%;}}</style>', 
        unsafe_allow_html=True
    )

    platform_settings = get_platform_settings(platform_admin_tenant)

    if 'hits' in platform_settings:
        platform_properties = platform_settings['hits']['hits'][0]['_source']

    platform_roles = platform_properties['roles']
    platform_models = platform_properties['models']['models']
    platform_pipelines = platform_properties['pipelines']['pipelines']

    platform_tenants = get_platform_tenants(platform_admin_tenant)

    tenant_doc = get_tenant_doc(platform_admin_tenant)
    doc =  tenant_doc['hits']['hits'][0]
    tenant_properties = tenant_doc['hits']['hits'][0]['_source']

    tenant_index = doc['_index']
    tenant_email = tenant_properties['email']
    tenant_roles = tenant_properties['roles']['roles']

    tab1, tab2, tab3 = st.tabs(["Tenant Data", "Profile", "Logs"])
    
    with tab1:
        col1, col2, col3, col4, col5, col6, col7 =  st.columns([3, 0.33, 2, 0.33, 4, 0.33, 3])

        with col1:
            flattened = [item for item in platform_tenants]
            option = st.selectbox(
                "Tenants",
                (flattened),
            )
            st.write("You selected:", option)
            if option:
                platform_files = get_platform_files(platform_admin_tenant)
                st.write(platform_files)
           
        with col3:
            st.text("Roles")
            flattened = [item["name"] for item in tenant_roles]
            tagger_component('', flattened)
           
        with col5:
            st.text("Models")
            flattened = [item["name"] for item in platform_models]
            tagger_component('', flattened)

        with col7:
            st.text("Pipelines")
            flattened = [item["name"] for item in platform_pipelines]
            tagger_component('', flattened)

    with tab2:
            
        with st.form("my_form"):
            
            name = st.text_input("Name", max_chars=50, value=tenant_properties['name'])
            given_name = st.text_input("Given Name", value=tenant_properties['given_name'], max_chars=50)

            roles = []
            for role in tenant_roles:
                roles.append(role['name'])

            all_roles = []
            for role in platform_roles['roles']:
                all_roles.append(role['name'])

            selected_roles = st.multiselect('Roles', all_roles, default=roles)
                
            submit_button = st.form_submit_button(label="Save")

            if submit_button:
                if len(selected_roles) == 0:
                    st.error('Must select at least one role')
                else: 
                    doc_id = tenant_doc['hits']['hits'][0]['_id']
                    role_updates = {}
                    role_updates['roles'] = []
                    for role in selected_roles:
                        role_updates['roles'].append({"name": role})

                    data = {
                        "mappings": {
                            "properties": {
                                "name": name,
                                "given_name": given_name,
                                "email": tenant_email,
                                "roles": role_updates
                            }
                        }
                    }

                    put_platform_doc(st.session_state['tenant_id'], doc_id, data)

    with tab3:
       
        platform_logs = get_logs(platform_admin_tenant)
        
        extracted_logs = []
        for l in platform_logs['hits']['hits']:
            extracted_logs.append(l['_source'])

        st.write(pd.json_normalize(extracted_logs))
        

