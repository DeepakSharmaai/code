import streamlit as st
import os
import fitz  # PyMuPDF
import docx
from io import StringIO
from openai import OpenAI
from openai import OpenAIError

# --- Streamlit UI Setup ---
st.set_page_config(page_title="📄 Document Summarizer", layout="wide")
st.title("📄 Document Summarizer using OpenAI")

# --- API Key Input ---
api_key = st.secrets["OPENAI_API_KEY"] or st.text_input("Enter your OpenAI API Key", type="password")
client = OpenAI(api_key=api_key) if api_key else None

# --- File Upload ---
uploaded_file = st.file_uploader("Upload a file (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])

# --- File Parsing Functions ---
def extract_text_from_pdf(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    except Exception as e:
        st.error(f"PDF extraction error: {e}")
        return ""

def extract_text_from_docx(file):
    try:
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        st.error(f"DOCX extraction error: {e}")
        return ""

def extract_text_from_txt(file):
    try:
        return file.read().decode("utf-8")
    except Exception as e:
        st.error(f"TXT extraction error: {e}")
        return ""

# --- Summarization Function using OpenAI v1.x ---
def summarize_text(text, model="gpt-4.1-mini", max_tokens=300):
    if not text.strip():
        return "No content to summarize."
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
                {"role": "user", "content": f"Please summarize the following:\n\n{text[:8000]}"}
            ],
            max_tokens=max_tokens,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        return f"OpenAI API error: {e}"

# --- Main App Logic ---
if uploaded_file:
    file_type = uploaded_file.type
    if "pdf" in file_type:
        full_text = extract_text_from_pdf(uploaded_file)
    elif "word" in file_type:
        full_text = extract_text_from_docx(uploaded_file)
    elif "text" in file_type:
        full_text = extract_text_from_txt(uploaded_file)
    else:
        full_text = ""

    if full_text:
        st.subheader("📃 Extracted Text")
        st.text_area("Document Preview", full_text[:2000], height=300)

        if client and st.button("🔍 Summarize"):
            with st.spinner("Summarizing with GPT..."):
                summary = summarize_text(full_text)
                st.success("✅ Summary")
                st.write(summary)
    else:
        st.error("Could not extract any text.")
