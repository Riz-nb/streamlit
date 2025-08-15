import streamlit as st
from extractor import extract_text_from_pdf
from llm import ask_question
from section_selector import detect_section

st.set_page_config(page_title="Bishop's Academic Calendar Assistant", layout="centered")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center;'>
    <h1> Bishop's Academic Calendar Assistant</h1>
    <p>Ask questions about the official Bishop’s University Academic Calendar.<br>
    Whether it's about  courses, deadlines,  exams, or 🎓 graduation requirements —<br>
    we’ve got you covered!</p>
            <br><br>
</div>
""", unsafe_allow_html=True)

st.markdown("####  Type your question about Bishop's Academic Calendar:")
question = st.text_input("e.g., When is the add/drop deadline?", label_visibility="collapsed")


if st.button(" Ask"):
    section = detect_section(question)
    st.markdown(f'<div class="section-box">📁 <strong>Detected Section:</strong> <code>{section}</code></div>', unsafe_allow_html=True)

    try:
        sanitized_section = section.replace(" ", "_")
        pdf_path = f"split_sections/{sanitized_section}.pdf"
        context = extract_text_from_pdf(pdf_path)
        answer = ask_question(context, question, model="llama-3.1-8b-instant")
        st.markdown(f'<div class="answer-box"> <strong>Answer:</strong><br><br>{answer}</div>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(" Could not find the selected PDF section.")