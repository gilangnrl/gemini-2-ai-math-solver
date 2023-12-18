import streamlit as st
import google.generativeai as genai
from api_dev import api 
from io import StringIO
from PIL import Image
# from api import api 

# reusable function
def show_img(img):
    h, w = img.size[0], img.size[1]
    img = img.resize(((round(h-h/2), round(w-w/2))))
    st.image(img, f'caption: {filename}')

# Configure the API key
genai.configure(api_key=api)
model_multimodal = genai.GenerativeModel('gemini-pro-vision')
model_text = genai.GenerativeModel('gemini-pro')

st.title('AI Math Solver')
st.write('''Welcome to the "Math AI Solver" website, your versatile guide to solving math problems effortlessly! Whether you prefer text or images, this intuitive platform caters to your needs.''')
final_response = None
filename = ''
img = []
image_input = None
# with st.sidebar:
with st.sidebar:
    question = st.text_area("Type your math problem here:")
    image_input = st.file_uploader("Or simply just upload an image here:")
    
if image_input is not None:
    filename = image_input.name
    img = Image.open(image_input)
    show_img(img)
    
with st.sidebar:
    if st.button('Generate'):
        formatted_prompt = """
        system: You are a Math Solver that will try to answer math question. User will give you some math question between elementery school until college level. Answer the question step by step, give some explanation for each step. Try to explain clearly.
        """
        if question is not None and image_input is not None:
            question = formatted_prompt + f"user question: {question}"
            response = model_multimodal.generate_content([question, img])
            final_response = response
        elif question is None or question == '':
            response = model_multimodal.generate_content(img)
            final_response = response
        else:
            question = formatted_prompt + f"user question: {question}"
            response = model_text.generate_content(question)
            final_response = response
st.write('Answer: ')
if final_response != None:
    st.write(final_response.text)

