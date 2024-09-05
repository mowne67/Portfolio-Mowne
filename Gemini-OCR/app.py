import streamlit as st
import google.generativeai as genai
import PIL.Image
#from ocr import ocr_func, llm
import cv2
import numpy as np
import os

api_key = st.secrets['GOOGLE_API_KEY']
genai.configure(api_key=api_key)
st.set_page_config(layout = 'wide')
with st.container():
    st.logo("https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg", link="https://www.linkedin.com/in/mowne")
    #st.logo("https://toppng.com/uploads/preview/github-logo-transparent-png-11659780101agvzsukgqz.png", link="https://github.com/mowne67/Portfolio-Mowne")

uploaded_file = st.file_uploader("Upload your image file", type=['png', 'jpg', 'jpeg'])


#api_key = st.text_input("Google API Key")

model = genai.GenerativeModel('gemini-1.5-flash')
def llm(image):
    image = PIL.Image.fromarray(image)
    response = model.generate_content(["Extract and provide all of the text written in the given image. Do not provide anything other than the text in the given image", image])
    return response.text

if (uploaded_file is not None) and (api_key is not None):

    file_bytes = uploaded_file.getvalue()
    np_arr = np.fromstring(file_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    col1, col2 = st.columns(2)
    if img is not None:
        col1.image(img, caption='Processed Image')

    # col1, col2 = st.columns(2)
    # col1.write("OCR - pytesseract")
    col2.title("LLM - Gemini")

    # Initialize variables to store results
    #if st.session_state.ocr_result is None:

    #st.session_state.llm_result = None

    # ocr_b = col1.button("Read", key=1)
    # if ocr_b:
    #     st.session_state.ocr_result = ocr(img)

    # llm_b = st.button("Read", key=2)
    # if llm_b:
    #     st.session_state.llm_result = llm(img)

    # if st.session_state.ocr_result:
    #     col1.success(st.session_state.ocr_result)
    # if st.session_state.llm_result:
    #     st.warning(st.session_state.llm_result)
    if col2.button("Read"):
        col2.success(llm(img))
