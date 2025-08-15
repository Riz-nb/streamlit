
from llm import summarize_text



def get_sample_summaries(text):
    return [
        ("llama3-8b", summarize_text(text, model="llama-3.1-8b-instant")),
        ("llama3-70b", summarize_text(text, model="llama3-70b-8192")),
        ("gemma2-9b", summarize_text(text, model="gemma2-9b-it"))  # Or replace if deprecated
    ]

def rank_summaries(summaries, judge_model="llama-3.1-8b-instant"):
    prompt = "Here are three summaries. Please rank them from best to worst based on clarity, accuracy, and completeness. Explain your ranking briefly.\n\n"
    for i, (model_name, summary) in enumerate(summaries):
        prompt += f"Summary {chr(65+i)} (from {model_name}):\n{summary}\n\n"
    response = summarize_text(prompt, model=judge_model)
    return response

def fuse_three_summaries(summary_list, model="llama-3.1-8b-instant"):
    prompt = f"""
You are given three summaries of the same document. Write a unified, clear, and non-redundant summary that best represents all of them:

Summary A:
{summary_list[0]}

Summary B:
{summary_list[1]}

Summary C:
{summary_list[2]}
"""
    return summarize_text(prompt, model=model)


def rate_summary(final_summary, model="llama-3.1-8b-instant"):
    prompt = f"""
Rate the following summary on a scale from 1 to 10 for clarity, completeness, and factual consistency. Then explain your score in 1-2 sentences.

Summary:
{final_summary}
"""
    return summarize_text(prompt, model=model)



