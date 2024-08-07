def chat():
    import streamlit as st

    from openai import OpenAI

    from helpers.config import openaikey
    from helpers.markdown import powered_by_openai

    client = OpenAI(api_key=openaikey)   

    if "messages_bot" not in st.session_state:
        st.session_state["messages_bot"] = [{"role": "assistant", "content": "Would you like to learn more about adding AI to your app?"}]
        
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
            
    st.markdown(powered_by_openai, unsafe_allow_html=True)

    for msg in st.session_state.messages_bot:
        if msg["role"] == 'assistant':
            st.chat_message(msg["role"],avatar="🕵️‍♀️").write(msg["content"])
        else:
            st.chat_message(msg["role"]).write(msg["content"])
            
    # if prompt := st.chat_input():
    #     if not openaikey:
    #         st.info("Please add your OpenAI API key to continue.")
    #         st.stop()

    #     st.session_state.messages_bot.append({"role": "user", "content": prompt})
    #     st.chat_message("user").write(prompt)
            
    #     response = client.chat.completions.create(model=st.session_state.openai_model, messages=st.session_state.messages_bot)
    #     msg = response.choices[0].message.content
            
    #     st.session_state.messages_bot.append({"role": "assistant", "content": msg})
    #     st.chat_message("assistant",avatar="🤖").write(msg)

   