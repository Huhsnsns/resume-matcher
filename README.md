# Resume & Job Matcher

A web app that compares a resume to a job posting using the Gemini API. It gives a match score, the skills you already have, the skills you're missing, and three suggestions to improve your resume.

## Features
- Match score out of 100
- Matched and missing skills
- Three tailored suggestions
- Automatic retries and model fallback when the AI service is busy

## Built with
Python, Streamlit, Google Gemini API

## How to run
1. Clone the repo and create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install dependencies:
   ```
   python -m pip install -r requirements.txt
   ```
3. Get a free API key from Google AI Studio and set it:
   ```
   setx GEMINI_API_KEY "your-key"
   ```
   Then reopen your terminal.
4. Start the app:
   ```
   python -m streamlit run app.py
   ```

## What I learned
- Calling an AI API from Python
- Getting structured JSON output from a model
- Handling errors, retries, and overloaded services
- Building a simple web interface with Streamlit
