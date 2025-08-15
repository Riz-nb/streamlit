import streamlit as st
from extractor import extract_text_from_pdf
from llm import summarize_text, ask_question
from PIL import Image
import base64

st.set_page_config(layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
        .logo { 
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        .logo-title {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .panel-title {
            font-weight: bold;
            background-color: #333333;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 20px;
            margin-bottom: 10px;
        }
        .output-box {
            border: 1px dashed gray;
            padding: 15px;
            min-height: 300px;
            font-size: 18px;
            border-radius: 5px;
            background-color: #1e1e1e;
            color: white;
        }
        .footer {
            text-align: center;
            margin-top: 60px;
            font-size: 14px;
            color: #aaa;
        }
        textarea {
            background-color: #1e1e1e !important;
            color: white !important;
        }
        .stButton>button {
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)
def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_path = "logo/BU-logo-purpleHR.png"  
logo_base64 = image_to_base64(logo_path)

st.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <img src="data:image/png;base64,{logo_base64}" width="400">
        <h3 style="color:white; margin-top: 10px; margin-left:20px">BU LLM PDF Assistant</h3>
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

# --- Extract Text and Layout ---
if uploaded_file:
    extracted_text = extract_text_from_pdf(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="panel-title">Any Question?</div>', unsafe_allow_html=True)
        question = st.text_area("", placeholder="Type your question here...", height=100, label_visibility="collapsed")
        if st.button("Get Answer"):
            with st.spinner("Generating answer..."):
                answer = ask_question(extracted_text, question, model="llama-3.1-8b-instant")
                st.markdown(f'<div class="output-box"><i>Answer</i><br>{answer}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="panel-title">Summarize this, please</div>', unsafe_allow_html=True)
        if st.button("Generate Summary"):
            with st.spinner("Summarizing..."):
                prompt = "Please summarize the following:\n\n" + extracted_text
                summary = summarize_text(prompt, model="llama-3.1-8b-instant")
                st.markdown(f'<div class="output-box"><i>Summary</i><br>{summary}</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown('<div class="footer">Copyright © BU. Version 0.1. Last update August 2025</div>', unsafe_allow_html=True)
