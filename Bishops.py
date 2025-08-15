# bishops.py
import base64
from pathlib import Path

import streamlit as st
from extractor import extract_text_from_pdf
from llm import ask_question, summarize_text
from section_selector import detect_section

st.set_page_config(page_title="Bishop's Academic Calendar Assistant", layout="wide")

# ---------- Styles ----------
st.markdown("""
    <style>
        /* Remove Streamlit's default page padding */
        [data-testid="stAppViewContainer"] .main .block-container {
            padding-left: 0 !important;
            padding-right: 0 !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }
        .panel-title {
            font-weight: 700;
            background-color: #333333;
            color: white;
            padding: 10px 12px;
            border-radius: 0;
            font-size: 20px;
            margin: 0 0 10px 0;
        }
        .output-box {
            border: 1px dashed gray;
            padding: 15px;
            min-height: 280px;
            font-size: 18px;
            border-radius: 0;
            background-color: #1e1e1e;
            color: white;
            margin: 0;
            white-space: pre-wrap;
        }
        .footer {
            text-align: center;
            margin-top: 48px;
            font-size: 14px;
            color: #aaa;
        }
        textarea, input, .stTextInput textarea {
            background-color: #1e1e1e !important;
            color: white !important;
        }
        .stButton>button {
            margin-top: 10px;
            width: 100%;
        }
        .section-pill {
            display:inline-block; padding:4px 8px; border:1px solid #666; border-radius:6px;
            background:#111; color:#ddd; font-size:14px; margin: 8px 0 12px 0;
        }
        /* Scroll container for the section list */
        .scroll-box {
            max-height: 360px;
            overflow-y: auto;
            border: 1px solid #444;
            border-radius: 8px;
            padding: 8px;
            background: #111;
        }
        /* 1) Global scale (shrinks everything: logo, fonts, inputs, buttons) */
        html { zoom: 0.90; }   /* try 0.85 for smaller, 0.95 for larger */

        /* 2) Fallback if a browser ignores zoom: reduce base font + headings */
        :root { font-size: 14px; }     /* default is ~16px */
        h1 { font-size: 1.6rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }

        /* 3) Make form controls a bit smaller too */
        button, input, textarea, select { font-size: 0.9rem !important; }

        /* Optional: slightly smaller panel header */
        .panel-title { font-size: 16px !important; padding: 6px 8px !important; }
    </style>
""", unsafe_allow_html=True)

# ---------- Helpers ----------
def image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def list_sections(dir_path="split_sections"):
    """Return nice display names for all PDFs in split_sections/."""
    p = Path(dir_path)
    if not p.exists():
        return []
    sections = sorted([pdf.stem.replace("_", " ") for pdf in p.glob("*.pdf")])
    return sections

@st.cache_data(show_spinner=False)
def load_pdf_text_cached(pdf_path: str) -> str:
    return extract_text_from_pdf(pdf_path)

# ---------- Header ----------
logo_path = "logo/BU-logo-purpleHR.png"
try:
    logo_b64 = image_to_base64(logo_path)
    st.markdown(
        f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; width:100%;">
            <img src="data:image/png;base64,{logo_b64}" width="400">
            <h3 style="color:white; margin-top:10px;">BU LLM PDF Assistant</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
except Exception:
    st.markdown("<h3 style='text-align:center'>BU LLM PDF Assistant</h3>", unsafe_allow_html=True)

# ---------- Layout: Ask (left) | Summarize (right) ----------
col1, col2 = st.columns(2, gap="small")

# ===== Left: Ask a question =====
with col1:
    st.markdown('<div class="panel-title">Ask about the Academic Calendar</div>', unsafe_allow_html=True)
    question = st.text_input("Type your question (e.g., When is the add/drop deadline?)", label_visibility="collapsed")

    if st.button("Ask", key="ask_btn"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            # Auto-detect the best section from the question
            section = detect_section(question)
            st.markdown(f'<span class="section-pill">📁 Detected section: <code>{section}</code></span>', unsafe_allow_html=True)
            sanitized = section.replace(" ", "_")
            pdf_path = f"split_sections/{sanitized}.pdf"
            try:
                context = load_pdf_text_cached(pdf_path)
                with st.spinner("Generating answer..."):
                    answer = ask_question(context, question, model="llama-3.1-8b-instant")
                st.text_area("Answer", value=answer, height=300)
            except FileNotFoundError:
                st.error(f"Could not find: {pdf_path}")

# ===== Right: Summarize a section (scrollable list) =====

# ===== Right: Summarize a section (dropdown + filter) =====
with col2:
    st.markdown('<div class="panel-title">Summarize a Section</div>', unsafe_allow_html=True)

    all_sections = list_sections()  # from earlier helper
    if not all_sections:
        st.error("No sections found in `split_sections/`. Make sure your PDFs are there.")
    else:
        # quick filter box (case-insensitive)
        q = st.text_input("Filter sections (e.g., Fees, Sessional, Admission)",
                          placeholder="type to filter…", key="filter_sections")

        filtered = [s for s in all_sections if q.lower() in s.lower()] if q else all_sections
        if not filtered:
            st.info("No sections match your filter.")
        else:
            # default to 'Fees' if present
            default_idx = (filtered.index("Fees") if "Fees" in filtered else 0)

            picked_section = st.selectbox(
                "Choose a section to summarize",
                filtered,
                index=default_idx,
                label_visibility="collapsed",
                help="This dropdown scrolls when the list is long."
            )

            if st.button("Summarize selected section", key="summarize_btn"):
                sanitized = picked_section.replace(" ", "_")
                pdf_path = f"split_sections/{sanitized}.pdf"
                try:
                    section_text = load_pdf_text_cached(pdf_path)
                    prompt = (
                        "Summarize the following Bishop's Academic Calendar in maximum 2 paragraphs and and dont say here is your summary or anything same. "
                        "Highlight important rules, key dates/deadlines, amounts/fees, and any critical conditions. "
                        "Be factual, avoid repetition, and keep it student-friendly.\n\n"
                        f"SECTION TEXT:\n\"\"\"\n{section_text}\n\"\"\"\n"
                    )
                    with st.spinner("Summarizing..."):
                        summary = summarize_text(prompt, model="llama-3.1-8b-instant")
                    st.text_area(f"Summary — {picked_section}", value=summary, height=300)

                except FileNotFoundError:
                    st.error(f"Could not find: {pdf_path}")


# ---------- Footer ----------
st.markdown('<div class="footer">Copyright © BU. Version 0.1. Last update August 2025</div>', unsafe_allow_html=True)
