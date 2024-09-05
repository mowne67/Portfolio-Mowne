from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOllama
import google.generativeai as genai
import streamlit as st
st.title("Talk to a CSV file!")
st.info('by Mowne')
st.logo("https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg",
        link="https://www.linkedin.com/in/mowne")
uploaded_file = st.file_uploader("Upload your Excel/CSV file", type=['xlsx', 'csv'])
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
        max_iterations = 1000
    )
    st.dataframe(df)
    question = st.text_input("Ask away!")
    if question:
        st.write_stream(agent_executor.invoke(question)['output'])

