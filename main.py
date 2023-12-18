import streamlit as st
import google.generativeai as genai
from PIL import Image
from api import api 

def show_img(img):
    h, w = img.size[0], img.size[1]
    img = img.resize(((round(h-h/2), round(w-w/2))))
    st.image(img, f'caption: {filename}')

latext = r'''
## Latex example
### full equation 
$$ 
\Delta G = \Delta\sigma \frac{a}{b} 
$$ 
### inline
Assume $\frac{a}{b}=1$ and $\sigma=0$...  
'''

# Configure the API key
genai.configure(api_key=api)
model_multimodal = genai.GenerativeModel('gemini-pro-vision')
model_text = genai.GenerativeModel('gemini-pro')

st.title('AI Math Solver')
st.write('''Welcome to the "Math AI Solver" website, your versatile guide to solving math problems effortlessly! Whether you prefer text or images, this intuitive platform caters to your needs.''')
final_response = None
filename = ''
img = []

with st.sidebar:
    question = st.text_area("Type your math problem here:", key='input_question')
    image_input = st.file_uploader("Or simply just upload an image here:", key='input_file')
    lang = option = st.selectbox(
        'What language should be use for the explanation?',
        (
            'English', 
            'Indonesian', 
            'Japanese',
            'France'
        )
    )
    
if question or image_input :
    st.session_state.disabled = False
else: 
    st.session_state.disabled = True

if image_input is not None:
    filename = image_input.name
    img = Image.open(image_input)
    show_img(img)
    
with st.sidebar:
    if st.button('Generate', key='button_submit', disabled=st.session_state.disabled):
        formatted_prompt = f"""
        
        Answer and explain the math question in detail, give step by step, write the answer in {lang} language, write with latext format without mention latext like example: {latext}
        """
        if question is not None and image_input is not None:
            question = f"user question: {question}" + formatted_prompt
            response = model_multimodal.generate_content([question, img])
            final_response = response
        elif question is None or question == '':
            response = model_multimodal.generate_content([formatted_prompt, img])
            final_response = response
        else:
            question = f"user question: {question}" + formatted_prompt
            response = model_text.generate_content(question)
            final_response = response
st.write('Answer: ')
if final_response != None:
    st.write(final_response.text)