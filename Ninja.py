import os
import requests
from dotenv import load_dotenv

load_dotenv()
NINJA_API_KEY = os.getenv('7wIDwwZr38n42f9Ya//WHg==pmHux4FNwD8VlKQS')

# -----------------------
# Function to compare two texts using API Ninjas
# -----------------------
def compute_similarity(text1, text2):
    if not text1.strip() or not text2.strip():
        return 0.0  # Avoid empty texts

    url = "https://api.api-ninjas.com/v1/textsimilarity"
    headers = {"X-Api-Key": os.getenv("NINJA_API_KEY")}
    data = {"text_1": text1, "text_2": text2}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print("❌ API Error:", response.text)  # For debugging
        return 0.0

    return response.json()["similarity"]

# -----------------------
# Generate similarity matrix from list of summaries
# -----------------------
def get_similarity_matrix(summaries):
    n = len(summaries)
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 1.0
            elif matrix[j][i] != 0.0:
                matrix[i][j] = matrix[j][i]
            else:
                # ⚠️ Truncate to 300 characters
                sim = compute_similarity(summaries[i][:300], summaries[j][:300])
                matrix[i][j] = sim

    return matrix


# -----------------------
# Find the most central summary
# -----------------------
def find_most_representative_summary(summaries, matrix):
    avg_similarities = [sum(row) / len(row) for row in matrix]
    best_index = avg_similarities.index(max(avg_similarities))
    return best_index, summaries[best_index]
