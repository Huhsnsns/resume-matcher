import time
from google import genai
from google.genai import errors

with open("resume.txt", "r") as f:
    resume = f.read()

with open("job.txt", "r") as f:
    job = f.read()

client = genai.Client()

prompt = f"""Compare this resume to the job posting.

RESUME:
{resume}

JOB POSTING:
{job}

Give me:
1. A match score out of 100
2. Skills from the job posting that the resume already shows
3. Skills the resume is missing
4. Three specific suggestions to improve the resume for this job
"""
models_to_try = ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3.5-flash"]

result_text = None
for model_name in models_to_try:
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            result_text = response.text
            print(f"(answered by {model_name})\n")
            break
        except errors.ServerError:
            print(f"{model_name} is busy, retrying (attempt {attempt + 1}/3)...")
            time.sleep(5)
        except errors.ClientError as e:
            print(f"{model_name} failed: {e}")
            break  # wrong model name or quota issue, move to the next model
    if result_text:
        break

if result_text:
    print(result_text)
else:
    print("All models are busy right now. Please try again in a few minutes.")