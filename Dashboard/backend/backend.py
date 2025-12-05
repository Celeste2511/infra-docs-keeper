# backend.py
from flask import Flask, request, jsonify
import os
import numpy as np
from PyPDF2 import PdfReader
from docx import Document
import faiss
from sentence_transformers import SentenceTransformer
from groq import Groq

app = Flask(__name__)

# Initialize models
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
groq_client = Groq(api_key="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")
llm_model = "llama-3.1-8b-instant"

# Global storage
chunks = []
index = None

def build_index_from_file(file_path):
    global chunks, index
    text = ""
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    # Split into chunks
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    vectors = np.vstack([embed_model.encode(c) for c in chunks]).astype("float32")
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

def retrieve(query, k=3):
    q_vec = embed_model.encode(query).reshape(1, -1).astype("float32")
    D, I = index.search(q_vec, k)
    return [chunks[i] for i in I[0]]

def ask_groq(query):
    context = "\n\n".join(retrieve(query))
    prompt = f"Use the following context to answer the question:\n{context}\n\nQuestion: {query}"
    chat = groq_client.chat.completions.create(
        model=llm_model,
        messages=[{"role": "user", "content": prompt}],
    )
    return chat.choices[0].message.content

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_type = file.filename.split(".")[-1].lower()
    save_path = os.path.join("./uploads", file.filename)
    os.makedirs("./uploads", exist_ok=True)
    file.save(save_path)

    # Build FAISS index for this file
    build_index_from_file(save_path)

    # Ask Groq for summary
    summary = ask_groq("Summarize this document")

    return jsonify({"summary": summary, "file_type": file_type})

if __name__ == "__main__":
    app.run(port=5000)
