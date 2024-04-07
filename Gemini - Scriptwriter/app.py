import streamlit as st
import google.generativeai as genai
from load_creds_github import load_creds
import pprint
st.set_page_config(layout="wide")
creds = load_creds()
genai.configure(credentials=creds)

model = genai.GenerativeModel(model_name=f'tunedModels/plot-writer')
st.title("CineMate")
st.write("Generate movie plots in no time!")
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        genre = st.text_area("Genre")
        tone = st.text_area("Tone")
        time_period = st.text_area("Time Period")
    with col2:
        outline = st.text_area("Plot Outline")
        char_info = st.text_area("Character Information")
        location = st.text_area("Location/Culture")
    with col3:
        purpose = st.text_area("Purpose")
        target = st.text_area("Target Audience")
        others = st.text_area("Extra Pointers")

prompt = f"""
Write a movie plot using the below information\n 
Genre: {genre} \n
Tone: {tone}\n 
Time Period: {time_period}\n 
Location/Culture: {location} \n
Outline: {outline} \n
Character Information: {char_info} \n
Purpose: {purpose}\n 
Target Audience: {target}\n
Other pointers: {others} \n
"""

if st.button("Generate Plot"):
    with st.spinner("Processing..."):
        plot = model.generate_content(prompt).text
        st.success(plot)
