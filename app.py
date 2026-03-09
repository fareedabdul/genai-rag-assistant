from flask import Flask, request, jsonify, render_template
from rag import build_vector_store, search
from groq import Groq
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()

# create flask app
app = Flask(__name__)

# initialize groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# build embeddings
build_vector_store()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.json
    message = data.get("message").lower()

    # greeting detection
    greetings = ["hello","hi","hey","good morning","good evening"]

    if any(greet in message for greet in greetings):
        return jsonify({
            "reply":"Hello! 👋 How can I assist you today?"
        })

    results = search(message)

    best_score = results[0][0]

    # similarity threshold
    if best_score < 0.35:
        return jsonify({
            "reply":"I’m sorry, I couldn't find relevant information in the knowledge base."
        })

    context = "\n".join([r[1]["content"] for r in results])

    prompt = f"""
Answer the question using ONLY the context below.

Context:
{context}

Question:
{message}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role":"user","content":prompt}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content

    return jsonify({
        "reply":answer
    })


if __name__ == "__main__":
    app.run(debug=True)