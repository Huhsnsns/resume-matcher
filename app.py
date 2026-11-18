import json
import time
import streamlit as st
from google import genai
from google.genai import errors, types

MODELS = ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3.5-flash"]


def analyze(resume, job):
    client = genai.Client()

    prompt = f"""You are a career coach. Compare this resume to the job posting.

Return JSON with exactly these keys:
- "score": an integer from 0 to 100
- "matched_skills": a list of skills from the job posting that the resume shows
- "missing_skills": a list of skills from the job posting that the resume lacks
- "suggestions": a list of exactly 3 specific suggestions to improve the resume

RESUME:
{resume}

JOB POSTING:
{job}
"""
    config = types.GenerateContentConfig(response_mime_type="application/json")

    for model_name in MODELS:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config,
                )
                return json.loads(response.text)
            except errors.ServerError:
                time.sleep(5)
            except json.JSONDecodeError:
                continue
            except errors.ClientError:
                break
    return None


st.set_page_config(page_title="Resume Matcher", page_icon="📄")
st.title("Resume & Job Matcher")
st.write("Paste your resume and a job posting to see how well they match.")

resume = st.text_area("Your resume", height=250)
job = st.text_area("Job posting", height=250)

if st.button("Analyze match"):
    if not resume.strip() or not job.strip():
        st.warning("Please paste both your resume and a job posting.")
    else:
        with st.spinner("Analyzing..."):
            data = analyze(resume, job)

        if data is None:
            st.error("The AI service is busy right now. Please try again in a few minutes.")
        else:
            score = max(0, min(100, int(data["score"])))
            st.metric("Match score", f"{score}/100")
            st.progress(score / 100)

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

                