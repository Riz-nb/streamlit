import os
from llm import ask_question  # Make sure this is your wrapper to call Groq or LLM
from extractor import extract_text_from_pdf

section_summaries = {}
pdf_dir = "./split_sections"  # This should be the folder containing your split PDF files

for file in os.listdir(pdf_dir):
    if file.endswith(".pdf"):
        section_name = file.replace(".pdf", "")
        file_path = os.path.join(pdf_dir, file)
        
        print(f"🔍 Summarizing: {section_name}")
        content = extract_text_from_pdf(file_path)
        
        summary_prompt = f"""Summarize the following academic calendar section for in maximum 3 sentences use in a navigation menu:\n\n{content}"""
        summary = ask_question(context="", question=summary_prompt, model="llama-3.1-8b-instant")
        section_summaries[section_name] = summary.strip()

# Save to JSON
import json
with open("section_summaries.json", "w") as f:
    json.dump(section_summaries, f, indent=2)

print("✅ All summaries saved to section_summaries.json")
