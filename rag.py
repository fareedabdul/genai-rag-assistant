import json
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

with open("docs.json") as f:
    documents = json.load(f)

vector_store = []

def generate_embedding(text):
    return model.encode(text)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def build_vector_store():

    for doc in documents:

        embedding = generate_embedding(doc["content"])

        vector_store.append({
            "title": doc["title"],
            "content": doc["content"],
            "embedding": embedding
        })

def search(query):

    query_embedding = generate_embedding(query)

    scores = []

    for item in vector_store:

        score = cosine_similarity(query_embedding, item["embedding"])

        scores.append((score, item))

    scores.sort(reverse=True)

    top_results = scores[:3]

    return top_results