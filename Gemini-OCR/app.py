import streamlit as st
import google.generativeai as genai
import PIL.Image
#from ocr import ocr_func, llm
import cv2
import numpy as np

st.set_page_config(layout = 'wide')
uploaded_file = st.file_uploader("Upload your image file", type=['png', 'jpg', 'jpeg'])

api_key = st.text_input("Google API Key")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro-vision')
def llm(image):
    image = PIL.Image.fromarray(image)
    response = model.generate_content(["Extract and provide all of the text written in the given image. Do not provide anything other than the text in the given image", image])
    return response.text

if (uploaded_file is not None) and (api_key is not None):

    file_bytes = uploaded_file.getvalue()
    np_arr = np.fromstring(file_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if img is not None:
        st.image(img, caption='Processed Image')

    # col1, col2 = st.columns(2)
    # col1.write("OCR - pytesseract")
    st.write("LLM - Gemini")

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
    if st.button("Read"):
        st.success(llm(img))
