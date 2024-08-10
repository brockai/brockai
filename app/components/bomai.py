def bomai():
    import streamlit as st

    from helpers.config import bomai_url
    
    tenant_id = 'bclayton403'
    url = f"{bomai_url}?id={tenant_id}"

    st.markdown(
        """
        <div className="iframe-container">
        <iframe className="responsive-iframe" src={url}" width="100%" height="100vh" style="border:none;"></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )
   