import streamlit as st
from extractor import extract_text_from_pdf
from llm import summarize_text, ask_question,fuse_summaries,evaluate_summaries_with_bertscore
from Ninja import get_similarity_matrix, find_most_representative_summary
from llmblender import get_sample_summaries,rate_summary,rank_summaries,fuse_three_summaries 
import json
import pandas as pd
import streamlit as st
import evaluate

st.title("LLMs PDF Summarizer & Questions")

uploaded_file = st.file_uploader("Your PDF", type="pdf")

if uploaded_file:
    with st.spinner("Extracting text..."):
        extracted_text = extract_text_from_pdf(uploaded_file)

    model_options = ["llama3-8b-8192", "llama3-70b-8192", "gemma2-9b-it"]

    st.markdown(" Model Settings")
    col1, col2 = st.columns(2)
    model_1 = col1.selectbox("Model 1", model_options, index=0)
    model_2 = col2.selectbox("Model 2", model_options, index=1)

    if st.button("Summaries"):
        with st.spinner("Generating summaries..."):
            text1 = extracted_text
            text2 = extracted_text

            summary1 = summarize_text("Please summarize the following:\n\n" +text1, model=model_1)
            summary2 = summarize_text("Please summarize the following:\n\n" +text2, model=model_2)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"  Summary from `{model_1}`")
            st.write(summary1)
        with col2:
            st.markdown(f"  Summary from `{model_2}`")
            st.write(summary2)

    st.subheader(" Compare Question Answers")
    question = st.text_input("Type a question to ask both models:")

    if st.button("Compare Answers"):
        with st.spinner("Asking both models..."):
            answer1 = ask_question(extracted_text, question, model=model_1)
            answer2 = ask_question(extracted_text, question, model=model_2)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Answer from `{model_1}`**")
            st.markdown(answer1)
        with col2:
            st.markdown(f"**Answer from `{model_2}`**")
            st.markdown(answer2)

    
    
    st.title("LLM Summary Fusion & Ranking Tool")
    if st.button(" Compute Similarity Matrix"):
        with st.spinner("Generating multiple summaries..."):
            models = ["llama3-8b-8192", "llama3-70b-8192", "gemma2-9b-it"]
            summaries = []
            for m in models:
                summary = summarize_text(extracted_text, model=m)
                summaries.append((m, summary))

        with st.spinner("Computing similarities..."):
            sim_matrix = get_similarity_matrix([s[1] for s in summaries])
            idx, best_summary = find_most_representative_summary([s[1] for s in summaries], sim_matrix)
            for model, summary in summaries:
                st.write(f"Model: {model}")
                st.write(summary)

        st.success(" Similarity analysis complete!")
        st.markdown(f"### 🏆 Most Representative Summary (from `{summaries[idx][0]}`)")
        st.write(best_summary)

        st.markdown(" Similarity Matrix:")
        for row in sim_matrix:
            st.text(["{:.2f}".format(val) for val in row])

    if st.button(" Fuse Summaries"):
        models = ["llama3-8b-8192", "llama3-70b-8192", "gemma2-9b-it"]
        summaries = []
        for m in models:
            summary = summarize_text(extracted_text, model=m)
            summaries.append((m, summary))
        with st.spinner("Merging all summaries..."):
            all_summaries = [s[1] for s in summaries]
            fused_summary = fuse_summaries(all_summaries)
        st.markdown("### 🧬 Fused Summary")
        st.write(fused_summary)
    summaries = get_sample_summaries(extracted_text)
    if st.button(" Rank 3 Summaries"):
        summaries = get_sample_summaries(extracted_text)
        ranking_result = rank_summaries(summaries)
        st.markdown(" Ranking Result")
        st.write(ranking_result)

    if st.button("Fuse All Summaries"):
        summaries = get_sample_summaries(extracted_text)
        all_texts = [s[1] for s in summaries]
        fused_result = fuse_three_summaries(all_texts)
        st.markdown("Fused Summary (3 models)")
        full_text = " ".join(all_texts)
        word_count = len(full_text.split())
        estimated_tokens = int(word_count * 1.3)
        st.write(estimated_tokens,fused_result)

    if st.button(" Rate Final Summary"):
        summaries = get_sample_summaries(extracted_text)
        all_texts = [s[1] for s in summaries]
        fused_result = fuse_three_summaries(all_texts)
        rating_result = rate_summary(fused_result)
        st.markdown(" Summary Rating")
        st.write(rating_result)

    st.set_page_config(page_title="QA Evaluation", layout="wide")
    st.set_page_config(page_title="QA Evaluation", layout="wide")
    st.title("📊 QA Evaluation with BERTScore")

    # Load the JSON file from the same folder
    try:
        with open("qa_test_cases.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        st.error(f"Could not read qa_test_cases.json: {e}")
        st.stop()

    # Normalize test cases
    test_cases = []
    for item in data:
        q = item.get("question", "")
        ref = item.get("answer", item.get("reference_answer", ""))
        ctx = item.get("context", "")
        test_cases.append({"context": ctx, "question": q, "reference_answer": ref})

    models = ["llama3-8b", "llama3-70b", "gemma2-9b"]

    if st.button("Run Evaluation"):
        results_table = []
        all_details = []

        for model in models:
            predictions = [ask_question(tc["context"], tc["question"], model) for tc in test_cases]
            bert_scores = evaluate_summaries_with_bertscore(
                predictions,
                [tc["reference_answer"] for tc in test_cases]
            )
            avg_bert = sum(bert_scores) / len(bert_scores)
            results_table.append({
                "Model": model,
                "Avg BERTScore": round(avg_bert, 3)
            })
            for tc, pred, score in zip(test_cases, predictions, bert_scores):
                all_details.append({
                    "Model": model,
                    "Question": tc["question"],
                    "Reference": tc["reference_answer"],
                    "Prediction": pred,
                    "BERTScore": score
                })

        # summary 
        st.subheader("Summary Metrics")
        df_summary = pd.DataFrame(results_table)
        st.dataframe(df_summary, use_container_width=True)

        st.subheader("Detailed Results (All Models)")
        df_details = pd.DataFrame(all_details)
        st.dataframe(df_details, use_container_width=True)

        # CSV downloads
        st.download_button("Download Summary CSV", df_summary.to_csv(index=False).encode("utf-8"),
                        file_name="summary_results.csv", mime="text/csv")
        st.download_button("Download Details CSV", df_details.to_csv(index=False).encode("utf-8"),
                        file_name="detailed_results.csv", mime="text/csv")