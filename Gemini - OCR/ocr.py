import cv2
import pytesseract
import matplotlib.pyplot as plt
import google.generativeai as genai
import PIL.Image

genai.configure(api_key="AIzaSyDS8BvpzKLnRwnpR1TVUuQUREdvDfOULgg")
model = genai.GenerativeModel('gemini-pro-vision')
exe_path = r"C:\Users\u1137734\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = exe_path

img = cv2.imread("sample_images/hw.jpg")
# img = cv2.resize(img, (400, 450))
plt.imshow(img)
text = pytesseract.image_to_string(img, lang='eng')
print(text)


def ocr(image):
    text = pytesseract.image_to_string(image, lang='eng')
    return text


def llm(image):
    image = PIL.Image.fromarray(image)
    response = model.generate_content(["What is the text written in the given image?", image])
    return response.text