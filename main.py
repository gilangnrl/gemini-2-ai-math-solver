import streamlit as st
import google.generativeai as genai
from api_dev import api 
# from api import api 

# Configure the API key
genai.configure(api_key=api)

# Set default parameters
defaults = {
    'model': 'models/text-bison-001',
    'temperature': 0.25,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
}

st.title('AI MATH TEACHER')
st.write('You can ask me to solve math question')
final_response = None

# with st.sidebar:
question = st.text_area("What is your problem")
if st.button('Generate'):
    formatted_prompt = f"""
    You are a Math teacher that will try to answer math question. User will give you some math question between elementery school until college level. Answer the question step by step, give some explanation for each step. Try to explain clearly.
    user question: {question}
    """
    response = genai.generate_text(
        **defaults,
        prompt=formatted_prompt
    )
    final_response = response
if final_response != None:
    st.write(final_response.result)

