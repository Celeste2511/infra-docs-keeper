import streamlit as st
import requests

st.title("Document Summarizer (PDF, DOCX, TXT)")

uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx", "txt"])

if uploaded_file:
    files = {"file": uploaded_file}

    try:
        response = requests.post("http://127.0.0.1:5000/upload", files=files)
        data = response.json()

        if response.status_code != 200:
            st.error(data.get("error", "Unknown error"))
        else:
            st.success("Summary generated!")

            st.subheader("Summary:")
            st.write(data["summary"])

            st.info(f"Detected File Type: {data['file_type']}")

    except Exception as e:
        st.error(f"Error communicating with backend: {e}")
