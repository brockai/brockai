def platform_admin():
    import streamlit as st
    import pandas as pd
    import streamlit_antd_components as sac

    from helpers.antd_utils import show_space
    from services.platform_service import get_platform_tenants, get_platform_settings, get_logs, put_platform_doc
    from services.tenant_service import get_tenant_doc
    from helpers.config import platform_admin_tenant 

    st.markdown(
        f'<style>.df .col-Name {{max-width: 100%;}}</style>', 
        unsafe_allow_html=True
    )

    if 'tab_index' not in st.session_state:
        st.session_state['tab_index'] = 0
    else:
        tab_index = st.session_state['tab_index']

    platform_settings = get_platform_settings(platform_admin_tenant)

    if 'hits' in platform_settings:
        platform_properties = platform_settings['hits']['hits'][0]['_source']

    platform_roles = platform_properties['roles']
    platform_models = platform_properties['models']['models']
    platform_pipelines = platform_properties['pipelines']['pipelines']

    platform_tenants = get_platform_tenants(platform_admin_tenant)

    tenant_doc = get_tenant_doc(st.session_state['tenant_id'])
    doc =  tenant_doc['hits']['hits'][0]
    tenant_properties = tenant_doc['hits']['hits'][0]['_source']

    tenant_index = doc['_index']
    tenant_email = tenant_properties['email']
    tenant_roles = tenant_properties['roles']['roles']

    for item in tenant_roles:
        not_admin = True
        if 'name' in item and item['name'] == 'admin':
            not_admin = False

    tab_index = sac.tabs([
        sac.TabsItem(label='Platform Settings', icon='gear'),
        sac.TabsItem(label='Vector Profile', icon='vector-pen'),
        sac.TabsItem(label='Platform Logs', icon='list-columns-reverse', disabled=not_admin)
    ], index=st.session_state['tab_index'], return_index=True, align='left')
    
    if tab_index  == 0:

        role_chip_items = []
        for role in platform_roles['roles']:
            role_chip_items.append(sac.ChipItem(label=role['name'], icon='people'))

        model_chip_items = []
        for model in platform_models:
            model_chip_items.append(sac.ChipItem(label=model['name'], icon='box'))

        pipeline_chip_items = []
        for pipeline in platform_pipelines:
            pipeline_chip_items.append(sac.ChipItem(label=pipeline['name'], icon='building-gear'))

        tenant_chip_items = []
        for tenant in platform_tenants:
            tenant_chip_items.append(sac.ChipItem(label=tenant, icon='vector-pen'))

        col1, col2, col3, col4, col5 =  st.columns([2, 0.25, 4, 0.25, 4])

        with col1:
            sac.chip(
                role_chip_items, label='Roles', align='left', radius='md', variant='outline'
            )

        with col3:
            sac.chip(
                model_chip_items, label='Models', align='left', radius='md', variant='outline'
            )

        with col5:
            sac.chip(
                pipeline_chip_items, label='Pipelines', align='left', radius='md', variant='outline'
            )

        show_space(1)
        sac.chip(
            tenant_chip_items, label='Vector Profiles', align='left', radius='md', variant='outline'
        )

    if tab_index == 1:
        
        with st.form("my_form"):
            
            st.write('Vector Index Root: ', tenant_index)
            st.write('Authentication Email: ', tenant_email)

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

    if tab_index == 2:

        platform_logs = get_logs(platform_admin_tenant)
        
        extracted_logs = []
        for l in platform_logs['hits']['hits']:
            extracted_logs.append(l['_source'])

        st.write(pd.json_normalize(extracted_logs))
        
            
