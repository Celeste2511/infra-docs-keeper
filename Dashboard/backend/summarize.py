
# !pip install faiss-cpu PyPDF2 python-docx sentence-transformers groq torch

import os
import numpy as np
from PyPDF2 import PdfReader
from docx import Document
import faiss
from sentence_transformers import SentenceTransformer
from groq import Groq

embed_model = SentenceTransformer("all-MiniLM-L6-v2")  # offline embeddings
groq_client = Groq(api_key="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")
llm_model = "llama-3.1-8b-instant"

folder_path = "./docs"  # folder with PDFs and DOCXs
file_names = [f for f in os.listdir(folder_path) if f.endswith(('.pdf', '.docx'))]
chunks = []

for f in file_names:
    path = os.path.join(folder_path, f)
    text = ""
    if f.endswith(".pdf"):
        reader = PdfReader(path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    elif f.endswith(".docx"):
        doc = Document(path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    
    text_chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    chunks.extend(text_chunks)

print(f"✅ Loaded {len(chunks)} chunks from {len(file_names)} files.")

vectors = np.vstack([embed_model.encode(c) for c in chunks]).astype('float32')
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)
print(f"✅ FAISS index ready with {len(chunks)} vectors.")

k_retrieve = 3
def retrieve(query, k=k_retrieve):
    q_vec = embed_model.encode(query).reshape(1, -1).astype('float32')
    D, I = index.search(q_vec, k)
    return [chunks[i] for i in I[0]]

def ask_groq(query):
    context = "\n\n".join(retrieve(query))
    prompt = f"Use the following context to answer the question:\n{context}\n\nQuestion: {query}"
    
    chat = groq_client.chat.completions.create(
        model=llm_model,
        messages=[{"role": "user", "content": prompt}]
    )
    return chat.choices[0].message.content

response = ask_groq("What is the document about?")
print("\n📝 LLM Response:\n", response)
