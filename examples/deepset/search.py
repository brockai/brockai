import streamlit as st
st.set_page_config(layout="wide")
import logging
import os

from annotated_text import annotation
from json import JSONDecodeError
from markdown import markdown
from config import parser, model_configs, document_store_choices
from helpers.haystack import start_document_store, start_all_document_stores, start_haystack_extractive, start_haystack_rag, query
from helpers.ui_state import reset_results, set_initial_state, set_model, set_store
from helpers.markdown import sidebar_links_footer, haystack_header

try:
    document_store = start_document_store(type = "In Memory")
    pipeline = start_haystack_rag(document_store)
  
    set_initial_state()
    
    options = {key: value for key, value in list(model_configs.items())[1:]}
    
    # sidebar
    selected_option = st.sidebar.selectbox('Choose a model',list(options.keys()), disabled=True)
    
    if selected_option:
        set_model(selected_option)
        selected_option_label = selected_option.replace("_", " ")
        
        if selected_option == 'EXTRACTIVE_MODEL':
            pipeline = start_haystack_extractive(document_store)
        else:
            pipeline = start_haystack_rag(document_store)
    
    selected_store = st.sidebar.selectbox('Choose a data store', document_store_choices, disabled=True)
        
    with open('styles.css') as f:
        st.sidebar.markdown(
            f'<style>{f.read()}</style>'
            +haystack_header
            +sidebar_links_footer
            , unsafe_allow_html=True
        )
        
    # main container
    st.title("👑 deepset Search Pipeline")
    
    st.header(selected_option_label)
    st.subheader(f"**{st.session_state['model']}**")
    question = st.text_input("Ask a question", value=st.session_state["question"], max_chars=100, on_change=reset_results)

    run_pressed = st.button("Run")

    # functions
    run_query = (
        run_pressed or question != st.session_state.question
    )

    # Get results for query
    if run_query and question:
        reset_results()
        st.session_state.question = question
        with st.spinner("🔎 &nbsp;&nbsp; Running your pipeline"):
            try:
                st.session_state.results = query(pipeline, question)
            except JSONDecodeError as je:
                st.error(
                    "👓 &nbsp;&nbsp; An error occurred reading the results. Is the document store working?"
                )    
            except Exception as e:
                logging.exception(e)
                st.error("🐞 &nbsp;&nbsp; An error occurred during the request.")
            
    if st.session_state.results:
        results = st.session_state.results
        
        if selected_option == 'EXTRACTIVE_MODEL':
            answers = results['answers']
            for count, answer in enumerate(answers):
                if answer.answer:
                    text, context = answer.answer, answer.context
                    start_idx = context.find(text)
                    end_idx = start_idx + len(text)
                    st.write(
                        markdown(context[:start_idx] + str(annotation(body=text, label="ANSWER", background="#964448", color='#ffffff')) + context[end_idx:]),
                        unsafe_allow_html=True,
                    )
                else:
                    st.info(
                        "🤔 &nbsp;&nbsp; Haystack is unsure whether any of the documents contain an answer to your question. Try to reformulate it!"
                    )
        elif selected_option == 'GENERATIVE_MODEL':
            st.write(results['results'][0])

except SystemExit as e:
    # This exception will be raised if --help or invalid command line arguments
    # are used. Currently streamlit prevents the program from exiting normally
    # so we have to do a hard exit.
    os._exit(e.code)

