"""The dashboard: resume matcher in the middle, side panel with chat, history and settings."""

import html
import time

import streamlit as st

import engine
import rewriter
import session
from sample_data import SAMPLE_JOB, SAMPLE_RESUME
from styles import h


# ------------------------------------------------------------------ helpers ---

def esc(text):
    return html.escape(str(text))


def short(text, limit=34):
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def chips(items, kind):
    if not items:
        return '<span class="muted">None found</span>'
    return "".join(f'<span class="chip chip-{kind}">{esc(i)}</span>' for i in items)


def verdict(score):
    if score >= 75:
        return "Strong match", "#16a34a"
    if score >= 50:
        return "Partial match", "#d97706"
    return "Needs work", "#dc2626"


def current_record():
    S = st.session_state
    if S.viewing_id is not None:
        for rec in S.analyses:
            if rec["id"] == S.viewing_id:
                return rec
    return S.analyses[0] if S.analyses else None


def report_text(record):
    r = record["result"]
    lines = [
        "RESUME MATCH REPORT",
        f"Resume: {record['resume_name']}",
        f"Job: {record['job_label']}",
        f"Match score: {r['score']}/100",
        "",
        "Skills you have:",
        *[f"  - {s}" for s in r["matched_skills"]],
        "",
        "Skills to add:",
        *[f"  - {s}" for s in r["missing_skills"]],
        "",
        "Suggestions:",
        *[f"  {i}. {s}" for i, s in enumerate(r["suggestions"], start=1)],
    ]
    return "\n".join(lines)


# ----------------------------------------------------------------- callbacks ---

def open_analysis(analysis_id):
    st.session_state.viewing_id = analysis_id


def back_to_latest():
    st.session_state.viewing_id = None


def start_new_chat():
    st.session_state.current_chat = None


def open_chat(chat_id):
    st.session_state.current_chat = chat_id
    st.session_state.side_panel = session.PANEL_CHAT


# ------------------------------------------------------------- run an analysis ---

def remember_files(uploads):
    S = st.session_state
    for u in uploads:
        known = any(
            f["name"] == u["name"] and f["role"] == u["role"] and f["size"] == u["size"]
            for f in S.files
        )
        if not known:
            S.files.insert(0, {**u, "ts": time.time()})


def run_and_store(resume_parts, job_parts, resume_name, job_label, uploads):
    S = st.session_state
    with st.spinner("Reading your documents and analyzing the match…"):
        out = engine.analyze(resume_parts, job_parts, S.settings)

    if out is None:
        reason = short(S.get("last_error") or "unknown reason", 250)
        st.error(f"The AI service didn't return a result. Reason: {reason}")
        return

    rec_id = session.new_id()
    S.sources[rec_id] = {"resume_parts": resume_parts, "job_parts": job_parts}
    S.analyses.insert(
        0,
        {
            "id": rec_id,
            "ts": time.time(),
            "resume_name": resume_name,
            "job_label": job_label,
            "result": out["result"],
            "model": out["model"],
            "seconds": out["seconds"],
        },
    )
    S.latest = {
        "result": out["result"],
        "resume_name": resume_name,
        "resume_text": engine.parts_to_text(resume_parts)[:6000],
        "job_text": engine.parts_to_text(job_parts)[:4000],
    }
    remember_files(uploads)
    S.viewing_id = None
    st.rerun()


# ------------------------------------------------------------------- results ---

def render_result(record):
    r = record["result"]
    label, color = verdict(r["score"])
    score = r["score"]
    resume_name = esc(record["resume_name"])
    job_label = esc(record["job_label"])

    st.markdown(
        h(
            f"""
            <div class="card result-head">
              <div class="ring" style="--p:{score};--c:{color}"><span>{score}</span></div>
              <div>
                <div class="verdict" style="color:{color}">{label}</div>
                <div class="meta">Resume: {resume_name}</div>
                <div class="meta">Job: {job_label}</div>
              </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    left, right = st.columns(2, gap="large")
    left.markdown(
        h(f'<div class="card"><div class="card-title">✅ Skills you have</div>{chips(r["matched_skills"], "ok")}</div>'),
        unsafe_allow_html=True,
    )
    right.markdown(
        h(f'<div class="card"><div class="card-title">➕ Skills to add</div>{chips(r["missing_skills"], "miss")}</div>'),
        unsafe_allow_html=True,
    )

    tips = "".join(
        f'<div class="tip"><div class="tip-n">{i}</div><div>{esc(t)}</div></div>'
        for i, t in enumerate(r["suggestions"], start=1)
    )
    st.markdown(h(f'<div class="card-title pad">💡 Suggestions</div>{tips}'), unsafe_allow_html=True)

    model = record["model"]
    seconds = record["seconds"]
    st.caption(f"Answered by {model} in {seconds:.1f} seconds")
    st.download_button(
        "Download report (.txt)",
        data=report_text(record),
        file_name="resume-match-report.txt",
        mime="text/plain",
    )


# --------------------------------------------------------------------- sidebar ---

def render_chat():
    S = st.session_state
    st.button("➕ New chat", key="new_chat", use_container_width=True, on_click=start_new_chat)

    chat = S.chats.get(S.current_chat)
    messages = chat["messages"] if chat else []

    box = st.container(height=420, border=False)
    with box:
        if not messages:
            st.caption(
                "Ask about your results, how to word a bullet point, or how to prepare "
                "for the interview. Run a match first for answers about your own resume."
            )
        for m in messages:
            with st.chat_message(m["role"]):
                st.markdown(m["content"])

    if S.chat_notice:
        st.warning(S.chat_notice)
        S.chat_notice = None

    prompt = st.chat_input("Ask your career coach…", key="coach_input")
    if not prompt:
        return
    if not engine.get_api_key():
        st.error("No Gemini API key found, so the chat can't answer yet.")
        return

    if chat is None:
        chat_id = session.new_id()
        chat = {"title": short(prompt, 40), "messages": [], "created": time.time()}
        S.chats[chat_id] = chat
        S.current_chat = chat_id
    chat["messages"].append({"role": "user", "content": prompt})

    with box:
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                reply = engine.chat_reply(chat["messages"], S.latest, S.settings)

    if reply:
        chat["messages"].append({"role": "assistant", "content": reply})
    else:
        chat["messages"].pop()  # keep the conversation clean so it can be resent
        reason = short(S.get("last_error") or "unknown reason", 200)
        S.chat_notice = f"That message didn't go through. Reason: {reason} You can resend it: {short(prompt, 80)}"
    st.rerun()


def render_history():
    S = st.session_state
    st.caption("History is kept for this visit only. Refreshing the page clears it.")

    st.markdown('<div class="side-head">Analyses</div>', unsafe_allow_html=True)
    if not S.analyses:
        st.caption("No analyses yet.")
    for rec in S.analyses:
        score = rec["result"]["score"]
        name = short(rec["resume_name"], 26)
        st.button(
            f"{score}/100 · {name}",
            key=f"an_{rec['id']}",
            on_click=open_analysis,
            args=(rec["id"],),
            use_container_width=True,
        )
        st.caption(f"{session.ago(rec['ts'])} · {short(rec['job_label'], 40)}")

    st.markdown('<div class="side-head">Chats</div>', unsafe_allow_html=True)
    if not S.chats:
        st.caption("No chats yet.")
    for chat_id, chat in reversed(list(S.chats.items())):
        st.button(
            f"💬 {chat['title']}",
            key=f"chat_{chat_id}",
            on_click=open_chat,
            args=(chat_id,),
            use_container_width=True,
        )
        count = len(chat["messages"])
        st.caption(f"{count} messages · {session.ago(chat['created'])}")

    st.markdown('<div class="side-head">Uploaded files</div>', unsafe_allow_html=True)
    if not S.files:
        st.caption("No files uploaded yet.")
    for f in S.files:
        size_kb = max(1, f["size"] // 1024)
        st.markdown(
            h(
                f"""
                <div class="file-row">📎 {esc(short(f['name'], 36))}
                <small>{esc(f['role'])} · {size_kb} KB · {session.ago(f['ts'])}</small></div>
                """
            ),
            unsafe_allow_html=True,
        )


def render_settings():
    S = st.session_state
    s = S.settings
    if s["model_choice"] not in engine.MODEL_CHOICES:
        s["model_choice"] = "Auto"

    s["model_choice"] = st.selectbox(
        "AI model",
        engine.MODEL_CHOICES,
        index=engine.MODEL_CHOICES.index(s["model_choice"]),
        help="Auto tries the fastest model first and switches if one is busy.",
    )
    s["fast_mode"] = st.toggle(
        "Fast mode",
        value=s["fast_mode"],
        help="Skips the model's extra thinking time for quicker answers.",
    )
    s["num_suggestions"] = st.slider("Number of suggestions", 3, 6, s["num_suggestions"])
    s["tone"] = st.radio(
        "Feedback style",
        ["Friendly", "Direct"],
        index=["Friendly", "Direct"].index(s["tone"]),
        horizontal=True,
    )
    st.divider()
    st.button("🗑 Clear all history", key="clear_hist", use_container_width=True, on_click=session.clear_history)
    st.caption("Settings apply to your next analysis and chat message.")


def render_sidebar():
    S = st.session_state
    with st.sidebar:
        st.markdown('<div class="side-brand">📄 ResumeMatch</div>', unsafe_allow_html=True)
        panel = st.segmented_control(
            "Panel",
            [session.PANEL_CHAT, session.PANEL_HISTORY, session.PANEL_SETTINGS],
            key="side_panel",
            label_visibility="collapsed",
        ) or session.PANEL_CHAT

        if panel == session.PANEL_HISTORY:
            render_history()
        elif panel == session.PANEL_SETTINGS:
            render_settings()
        else:
            render_chat()


# ----------------------------------------------------------------- main area ---

def render():
    S = st.session_state
    render_sidebar()

    top = st.columns([6, 1.2], vertical_alignment="center")
    top[0].markdown(
        h(
            """
            <div class="dash-title">Resume Matcher</div>
            <div class="dash-sub">Compare your resume with a job description and see where you stand.</div>
            """
        ),
        unsafe_allow_html=True,
    )
    top[1].button("← Home", key="home_btn", use_container_width=True, on_click=session.go, args=("landing",))

    has_key = bool(engine.get_api_key())
    if not has_key:
        st.error(
            "No Gemini API key found. Set the GEMINI_API_KEY environment variable "
            "(or add it to Streamlit secrets when deployed), then restart the app."
        )

    # ---- inputs
    with st.container(border=True):
        col_resume, col_job = st.columns(2, gap="large")
        with col_resume:
            st.markdown("**1 · Your resume**")
            resume_file = st.file_uploader(
                "Resume file",
                type=engine.ALLOWED_TYPES,
                key="resume_file",
                label_visibility="collapsed",
                help="PDF, image, Word or text. Up to 10 MB.",
            )
        with col_job:
            st.markdown("**2 · Job description**")
            tab_paste, tab_file = st.tabs(["Paste text", "Upload file"])
            with tab_paste:
                job_text = st.text_area(
                    "Job description text",
                    height=150,
                    key="job_text",
                    label_visibility="collapsed",
                    placeholder="Paste the job description here…",
                )
            with tab_file:
                job_file = st.file_uploader(
                    "Job description file",
                    type=engine.ALLOWED_TYPES,
                    key="job_file",
                    label_visibility="collapsed",
                    help="PDF, screenshot, Word or text. You can use this and the text box together.",
                )

        btn_main, btn_sample = st.columns([3, 1.3])
        analyze_clicked = btn_main.button(
            "Analyze match", key="analyze_btn", type="primary", use_container_width=True, disabled=not has_key
        )
        sample_clicked = btn_sample.button(
            "Try sample data", key="sample_btn", use_container_width=True, disabled=not has_key
        )

    if sample_clicked:
        run_and_store([SAMPLE_RESUME], [SAMPLE_JOB], "Sample resume", "Sample job description", [])
    elif analyze_clicked:
        if resume_file is None:
            st.warning("Please upload your resume.")
        elif not job_text.strip() and job_file is None:
            st.warning("Please paste the job description or upload it as a file.")
        elif engine.too_big(resume_file) or (job_file is not None and engine.too_big(job_file)):
            st.error(f"Files must be smaller than {engine.MAX_FILE_MB} MB each.")
        else:
            try:
                resume_parts = engine.file_to_parts(resume_file)
                job_parts = []
                if job_text.strip():
                    job_parts.append(job_text)
                if job_file is not None:
                    job_parts += engine.file_to_parts(job_file)
            except Exception:
                resume_parts, job_parts = [], []

            if not resume_parts or not job_parts:
                st.error("I couldn't read one of the files. Try saving it again as a PDF or image.")
            else:
                job_label = short(job_text, 60) if job_text.strip() else job_file.name
                uploads = [{"name": resume_file.name, "role": "Resume", "size": resume_file.size}]
                if job_file is not None:
                    uploads.append({"name": job_file.name, "role": "Job description", "size": job_file.size})
                run_and_store(resume_parts, job_parts, resume_file.name, job_label, uploads)

    # ---- results
    record = current_record()
    if record is None:
        st.markdown(
            h(
                """
                <div class="empty"><b>Your results will appear here</b>
                Upload a resume and add a job description, or try the sample data.</div>
                """
            ),
            unsafe_allow_html=True,
        )
        return

    if S.viewing_id is not None and record is not S.analyses[0]:
        st.info("You're viewing an earlier result.")
        st.button("Back to latest result", key="back_latest", on_click=back_to_latest)

    render_result(record)
    rewriter.render_section(record)