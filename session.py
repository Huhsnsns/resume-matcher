"""Session state: everything here lives only for the current visit."""

import time

import streamlit as st

PANEL_CHAT = "💬 Chat"
PANEL_HISTORY = "🕘 History"
PANEL_SETTINGS = "⚙️ Settings"

DEFAULT_SETTINGS = {
    "model_choice": "Auto",
    "fast_mode": True,
    "num_suggestions": 3,
    "tone": "Friendly",
}


def init_state():
    ss = st.session_state
    ss.setdefault("page", "landing")
    ss.setdefault("settings", dict(DEFAULT_SETTINGS))
    ss.setdefault("analyses", [])      # newest first
    ss.setdefault("files", [])         # metadata only, never the file contents
    ss.setdefault("chats", {})         # id -> {"title", "messages", "created"}
    ss.setdefault("current_chat", None)
    ss.setdefault("viewing_id", None)  # None means "show the newest result"
    ss.setdefault("latest", None)      # context handed to the chatbot
    ss.setdefault("side_panel", PANEL_CHAT)
    ss.setdefault("chat_notice", None)
    ss.setdefault("next_id", 1)
    ss.setdefault("sources", {})       # analysis id -> the resume/job parts it used
    ss.setdefault("rewrites", {})      # analysis id -> rewriter output


def go(page):
    st.session_state.page = page


def new_id():
    n = st.session_state.next_id
    st.session_state.next_id += 1
    return n


def ago(ts):
    secs = int(time.time() - ts)
    if secs < 60:
        return "just now"
    if secs < 3600:
        return f"{secs // 60} min ago"
    return f"{secs // 3600} h ago"


def clear_history():
    ss = st.session_state
    ss.analyses = []
    ss.files = []
    ss.chats = {}
    ss.current_chat = None
    ss.viewing_id = None
    ss.latest = None
    ss.chat_notice = None
    ss.sources = {}
    ss.rewrites = {}