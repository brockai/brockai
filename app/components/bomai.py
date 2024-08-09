def bomai():
    import streamlit as st

    tenant_id = "your_tenant_id_here"

    st.markdown(
        """
        <div className="iframe-container">
        <iframe className="responsive-iframe" src="http://localhost:3000?id=${tenant_id}" width="100%" height="100vh" style="border:none;"></iframe>
        </div>
        """,
        unsafe_allow_html=True
    )
   