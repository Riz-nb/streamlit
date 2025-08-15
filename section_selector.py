import json
from llm import ask_question

with open("section_summaries.json", "r") as f:
    section_descriptions = json.load(f)

section_names = list(section_descriptions.keys())

def detect_section(question):
    section_info = "\n".join(f"- {name.replace('_', ' ')}: {desc}" for name, desc in section_descriptions.items())
    
    prompt = f"""You are helping route student questions to the correct section of an academic calendar.
Below is a list of available sections with a short explanation:

{section_info}

Question:
"{question}"

Please return only the most relevant section name exactly as shown above (case-sensitive).
"""
    section = ask_question(context="", question=prompt, model="llama-3.1-8b-instant")
    return section.strip()
