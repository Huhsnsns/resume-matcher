import io
import json
import os
import time
import streamlit as st
from google import genai
from google.genai import errors, types
from pypdf import PdfReader
from docx import Document

MODELS = ["gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-3.5-flash"]

IMAGE_TYPES = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "webp": "image/webp",
}
ALLOWED_TYPES = ["pdf", "png", "jpg", "jpeg", "webp", "docx", "txt"]
MAX_FILE_MB = 10


def file_to_parts(uploaded_file):
    """Turn an uploaded file into pieces the AI can read (text or file data)."""
    name = uploaded_file.name.lower()
    ext = name.rsplit(".", 1)[-1]
    data = uploaded_file.getvalue()

    if ext == "pdf":
        # Fast path: if the PDF has real text, send just the text.
        try:
            reader = PdfReader(io.BytesIO(data))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception:
            text = ""
        if len(text.strip()) >= 100:
            return [text]
        # Scanned PDF: send the PDF itself so Gemini can read the pages.
        return [types.Part.from_bytes(data=data, mime_type="application/pdf")]

    if ext in IMAGE_TYPES:
        return [types.Part.from_bytes(data=data, mime_type=IMAGE_TYPES[ext])]

    if ext == "docx":
        doc = Document(io.BytesIO(data))
        return ["\n".join(p.text for p in doc.paragraphs)]

    if ext == "txt":
        return [data.decode("utf-8", errors="ignore")]

    return []


def too_big(uploaded_file):
    return uploaded_file.size > MAX_FILE_MB * 1024 * 1024


def get_client():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = os.environ.get("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)


def analyze(resume_parts, job_parts):
    client = get_client()

    instructions = """You are a career coach. Compare the resume to the job description below.
Either one may be provided as text, an image, or a document. Read them carefully.

Return JSON with exactly these keys:
- "score": an integer from 0 to 100
- "matched_skills": a list of skills from the job description that the resume shows
- "missing_skills": a list of skills from the job description that the resume lacks
- "suggestions": a list of exactly 3 specific suggestions to improve the resume
"""
    contents = [instructions, "RESUME:"] + resume_parts + ["JOB DESCRIPTION:"] + job_parts

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    )

    for model_name in MODELS:
        for attempt in range(2):
            start = time.time()
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=config,
                )
                data = json.loads(response.text)
                return data, model_name, time.time() - start
            except errors.ServerError:
                print(f"{model_name} busy (attempt {attempt + 1})")
                time.sleep(2)
            except json.JSONDecodeError:
                print(f"{model_name} returned invalid JSON")
                continue
            except errors.ClientError as e:
                print(f"{model_name} failed: {e}")
                break
    return None, None, None


st.set_page_config(page_title="Resume Matcher", page_icon="📄")
st.title("Resume & Job Matcher")
st.write("Upload your resume and add a job description to see how well they match.")
st.caption(
    "Your files and text are sent to Google's Gemini API for analysis. "
    "Avoid uploading anything you wouldn't want shared."
)

st.subheader("1. Your resume")
resume_file = st.file_uploader(
    "Upload your resume (PDF, image, Word, or text)",
    type=ALLOWED_TYPES,
    key="resume_file",
)

st.subheader("2. Job description")
job_text = st.text_area("Paste the job description", height=200)
job_file = st.file_uploader(
    "...or upload it (PDF, image, Word, or text)",
    type=ALLOWED_TYPES,
    key="job_file",
)

if st.button("Analyze match"):
    if resume_file is None:
        st.warning("Please upload your resume.")
    elif not job_text.strip() and job_file is None:
        st.warning("Please paste the job description or upload it as a file.")
    elif too_big(resume_file) or (job_file is not None and too_big(job_file)):
        st.error(f"Files must be smaller than {MAX_FILE_MB} MB each.")
    else:
        try:
            resume_parts = file_to_parts(resume_file)
            job_parts = []
            if job_text.strip():
                job_parts.append(job_text)
            if job_file is not None:
                job_parts += file_to_parts(job_file)
        except Exception:
            resume_parts, job_parts = [], []

        if not resume_parts or not job_parts:
            st.error("I couldn't read one of the files. Try saving it again as a PDF or image.")
        else:
            with st.spinner("Analyzing..."):
                data, model_used, seconds = analyze(resume_parts, job_parts)

            if data is None:
                st.error("The AI service is busy right now. Please try again in a few minutes.")
            else:
                score = max(0, min(100, int(data["score"])))
                st.metric("Match score", f"{score}/100")
                st.progress(score / 100)
                st.caption(f"Answered by {model_used} in {seconds:.1f} seconds")

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Skills you have")
                    for skill in data["matched_skills"]:
                        st.write(f"✅ {skill}")
                with col2:
                    st.subheader("Skills to add")
                    for skill in data["missing_skills"]:
                        st.write(f"➕ {skill}")

                st.subheader("Suggestions")
                for i, tip in enumerate(data["suggestions"], start=1):
                    st.write(f"{i}. {tip}")