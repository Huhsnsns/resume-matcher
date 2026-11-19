"""The scrollable landing page."""

import streamlit as st

import session
from styles import h


def start_button(key, label="Get started free →"):
    _, mid, _ = st.columns([2, 1.6, 2])
    mid.button(
        label,
        key=key,
        type="primary" if key != "cta_final" else "secondary",
        use_container_width=True,
        on_click=session.go,
        args=("dashboard",),
    )


def render():
    # ---- top bar
    left, right = st.columns([5, 1.3], vertical_alignment="center")
    left.markdown(
        h('<div class="brand"><span class="logo">📄</span> ResumeMatch</div>'),
        unsafe_allow_html=True,
    )
    right.button(
        "Launch app",
        key="nav_launch",
        use_container_width=True,
        on_click=session.go,
        args=("dashboard",),
    )

    # ---- hero
    with st.container(key="hero"):
        st.markdown(
            h(
                """
                <div class="badge">✨ Powered by Google Gemini</div>
                <div class="hero-title">Know how well your resume fits <span class="grad">before you apply</span></div>
                <div class="lead">Upload your resume, add a job description, and get a match score,
                the skills you're missing, and clear suggestions to improve it, all in one place.</div>
                """
            ),
            unsafe_allow_html=True,
        )
        start_button("cta_hero")
        st.markdown(
            h('<div class="hero-note">No sign-up needed · PDF, image or Word files · Try it with sample data</div>'),
            unsafe_allow_html=True,
        )

    # ---- illustrative preview
    st.markdown(
        h(
            """
            <div class="mock-wrap">
              <div class="mock-label">Illustrative example of a result</div>
              <div class="card mock">
                <div class="result-head">
                  <div class="ring" style="--p:78;--c:#16a34a"><span>78</span></div>
                  <div>
                    <div class="verdict" style="color:#16a34a">Strong match</div>
                    <div class="meta">Resume: sample_resume.pdf</div>
                    <div class="meta">Job: Junior Software Engineer</div>
                  </div>
                </div>
                <div class="card-title">✅ Skills you have</div>
                <span class="chip chip-ok">Python</span><span class="chip chip-ok">SQL</span>
                <span class="chip chip-ok">REST APIs</span><span class="chip chip-ok">Git</span>
                <div class="card-title" style="margin-top:.9rem">➕ Skills to add</div>
                <span class="chip chip-miss">Docker</span><span class="chip chip-miss">AWS</span>
                <span class="chip chip-miss">CI/CD</span>
              </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # ---- how it works
    st.markdown(
        h(
            """
            <div class="section">
              <div class="section-title">How it works</div>
              <div class="section-sub">Three quick steps from upload to a sharper resume.</div>
              <div class="grid3">
                <div class="card"><div class="step-n">1</div><h4>Upload your resume</h4>
                  <p>Drop in a PDF, a photo or screenshot, a Word file, or plain text.</p></div>
                <div class="card"><div class="step-n">2</div><h4>Add the job description</h4>
                  <p>Paste the text, or upload it as a PDF or a screenshot of the posting.</p></div>
                <div class="card"><div class="step-n">3</div><h4>Get your match</h4>
                  <p>See your score, the skill gaps, and specific ways to improve your resume.</p></div>
              </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # ---- features
    st.markdown(
        h(
            """
            <div class="section">
              <div class="section-title">Everything you need to tailor your resume</div>
              <div class="section-sub">A focused toolkit, with nothing to install and no account to create.</div>
              <div class="grid3">
                <div class="card"><div class="icon-tile">🎯</div><h4>Match score</h4>
                  <p>A clear 0 to 100 score for how well your resume fits the role.</p></div>
                <div class="card"><div class="icon-tile">🧩</div><h4>Skill gap analysis</h4>
                  <p>See which required skills you already show and which are missing.</p></div>
                <div class="card"><div class="icon-tile">✍️</div><h4>Actionable suggestions</h4>
                  <p>Specific edits to tailor your resume to the job you want.</p></div>
                <div class="card"><div class="icon-tile">📎</div><h4>Any format</h4>
                  <p>PDFs, photos, screenshots, Word and text files, for both the resume and the job.</p></div>
                <div class="card"><div class="icon-tile">💬</div><h4>Career coach chat</h4>
                  <p>Ask follow-up questions about your results and how to improve them.</p></div>
                <div class="card"><div class="icon-tile">🕘</div><h4>History and settings</h4>
                  <p>Revisit earlier results during your visit and tune how the AI responds.</p></div>
              </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # ---- FAQ
    st.markdown(
        h('<div class="section"><div class="section-title">Questions</div><div class="section-sub"></div></div>'),
        unsafe_allow_html=True,
    )
    with st.expander("Is my data stored?"):
        st.write(
            "The app doesn't save your files to a database. Your history lives only for "
            "the current visit and is cleared when you refresh the page. Your files and "
            "text are sent to Google's Gemini API to be analyzed, so check Google's terms "
            "for how the API handles data, and avoid uploading anything you wouldn't want shared."
        )
    with st.expander("Which file types work?"):
        st.write(
            "PDF, PNG, JPG, WEBP, Word (.docx) and plain text, up to 10 MB each. "
            "Clear, high-resolution images give the best results."
        )
    with st.expander("How accurate is the score?"):
        st.write(
            "The score is an AI-generated estimate to help you compare and improve. It is "
            "not a prediction of what any employer's hiring system will do. Treat the skill "
            "gaps and suggestions as guidance and use your own judgment."
        )
    with st.expander("Why does it sometimes say the service is busy?"):
        st.write(
            "The app uses a shared free API quota. If a model is overloaded, it retries "
            "and switches to another model automatically. If everything is busy, wait a "
            "minute and try again."
        )

    # ---- final call to action
    with st.container(key="cta_band"):
        st.markdown(
            h(
                """
                <div class="cta-title">Ready to see how you match?</div>
                <div class="cta-sub">Open the dashboard and try it with your resume, or with sample data.</div>
                """
            ),
            unsafe_allow_html=True,
        )
        start_button("cta_final", "Open the dashboard →")

    st.markdown(
        h('<div class="footer">Built with Python, Streamlit and Google Gemini · A portfolio project</div>'),
        unsafe_allow_html=True,
    )
