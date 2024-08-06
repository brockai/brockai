def regcheck():
    import streamlit as st
    
    st.markdown(
    """
    <iframe src="http://localhost:3000?id=${tenant_id}" width="100%" height="800px" style="border:none;"></iframe>
    """,
    unsafe_allow_html=True
)
   