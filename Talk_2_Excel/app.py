from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOllama
import google.generativeai as genai
import streamlit as st

uploaded_file = st.file_uploader("Upload your Excel/CSV file", type=['xlsx', 'csv'])
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
st.success(agent_executor.invoke(question)['output'])

