def preprocessing_service():
    import streamlit as st

    # from opensearchpy import OpenSearch
    from helpers.config import client
    from services.s3api import upload_files
    from services.platform_service import platform_log
    from services.tenant_service import get_tenant_file
    from helpers.config import platform_admin_tenant


    file = get_tenant_file(st.session_state['tenant_id'], 'NPddwo0Bs3h86QjiE4I5')

    st.write(file)
