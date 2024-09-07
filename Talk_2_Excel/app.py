from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOllama
import google.generativeai as genai
import streamlit as st
import time

st.title("Talk to a CSV file!")
st.info('by Mowne')
st.logo("https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg",
        link="https://www.linkedin.com/in/mowne")
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    api_key = st.secrets['GOOGLE_API_KEY']
    genai.configure(api_key=api_key)

    llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash')
    agent_executor = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        allow_dangerous_code=True,
        handle_parsing_errors=True,
        max_iterations=1000
    )
    col1, col2 = st.columns()
    with col1:
        st.dataframe(df)
    question = st.text_input("Ask away!")
    if question:
        answer = agent_executor.invoke(question)['output']
        def stream_data():
            for word in answer.split(" "):
                yield word + " "
                time.sleep(0.02)
        st.write_stream(stream_data)
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    user_input = st.chat_input("Say something")
    with col2:
        if user_input:
            st.session_state['chat_history'].append({'user': user_input})
            bot_response = agent_executor.invoke(user_input)['output']
            st.session_state['chat_history'].append({'bot': bot_response})

        for chat in st.session_state['chat_history']:
            if 'user' in chat:
                with st.chat_message('user'):
                    st.write(chat['user'], unsafe_allow_html=True)
            elif 'bot' in chat:
                with st.chat_message('assistant'):
                    st.write(str(chat['bot']), unsafe_allow_html=True)

