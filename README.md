# infra-docs-keeper
InfraDocs Keeper

InfraDocs Keeper is a small project we built to make it easier to understand long documents. You can upload a PDF, DOCX, or TXT file, and the app will generate a summary for you. It uses a Flask backend and a Streamlit frontend. The backend processes the file, extracts the text, and sends it to a Groq LLM to generate the final summary.

The goal is to quickly understand safety, maintenance, and compliance documents without reading the whole thing.

Features

Upload PDF, DOCX, or TXT files

Automatically extracts text

Summarizes using Groq’s Llama 3 model

Simple and clean Streamlit UI

Uses FAISS + embeddings for better context understanding

How to Run
1. Backend


Install the requirements:

pip install -r requirements.txt


Go into the backend folder:

cd backend



Add your Groq API key as an environment variable:

set GROQ_API_KEY=your_key_here     (Windows)
export GROQ_API_KEY=your_key_here  (Mac/Linux)


Start the backend:

python backend.py


You should see:

Running on http://127.0.0.1:5000


Leave this running.

2. Frontend

Open a new terminal and go to:

cd frontend



Start the frontend:

streamlit run app.py


This will open the UI in your browser.
