"""CSS for the landing page and the dashboard."""

import streamlit as st


def h(markup):
    """Put HTML on one line so Markdown never mistakes it for a code block."""
    return " ".join(line.strip() for line in markup.strip().splitlines() if line.strip())


COMMON_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
  --ink: #0f172a; --muted: #64748b; --line: #e2e8f0;
  --brand: #4f46e5; --brand2: #7c3aed; --soft: #f8fafc;
}
.stApp, .stMarkdown, .stButton button, .stTextArea textarea, .stCaption {
  font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
}
footer { visibility: hidden; }
.stButton button { border-radius: 12px; font-weight: 600; }

.muted { color: var(--muted); }
.card {
  background: #fff; border: 1px solid var(--line); border-radius: 18px;
  padding: 1.25rem 1.4rem; box-shadow: 0 1px 2px rgba(15, 23, 42, .04);
  height: 100%;
}
.card-title { font-weight: 700; color: var(--ink); margin-bottom: .6rem; }
.card-title.pad { margin: 1.4rem 0 .7rem; font-size: 1.05rem; }

.chip {
  display: inline-block; padding: .25rem .75rem; border-radius: 999px;
  font-size: .85rem; font-weight: 500; margin: .15rem .25rem .15rem 0;
}
.chip-ok { background: #dcfce7; color: #166534; }
.chip-miss { background: #fef3c7; color: #92400e; }

.ring {
  --p: 0; --c: #4f46e5;
  width: 112px; height: 112px; border-radius: 50%; flex: none;
  background: conic-gradient(var(--c) calc(var(--p) * 1%), #e2e8f0 0);
  display: grid; place-items: center; position: relative;
}
.ring::before { content: ""; position: absolute; inset: 10px; background: #fff; border-radius: 50%; }
.ring span { position: relative; font-size: 2rem; font-weight: 800; color: var(--ink); }
.result-head { display: flex; align-items: center; gap: 1.4rem; margin-bottom: 1rem; height: auto; }
.verdict { font-size: 1.5rem; font-weight: 800; letter-spacing: -.01em; }
.meta { color: var(--muted); font-size: .9rem; margin-top: .15rem; }

.tip {
  display: flex; gap: .9rem; align-items: flex-start; padding: .9rem 1rem;
  border: 1px solid var(--line); border-radius: 14px; background: #fff;
  margin-bottom: .6rem; color: var(--ink); line-height: 1.5;
}
.tip-n {
  flex: none; width: 28px; height: 28px; border-radius: 50%; display: grid;
  place-items: center; background: #eef2ff; color: var(--brand); font-weight: 700; font-size: .9rem;
}
"""

LANDING_CSS = """
.block-container { max-width: 1120px; padding-top: 1rem; }
header[data-testid="stHeader"] { background: transparent; }

.brand { font-weight: 800; font-size: 1.3rem; color: var(--ink); display: flex; align-items: center; gap: .5rem; padding-top: .35rem; }
.logo { display: inline-grid; place-items: center; width: 34px; height: 34px; border-radius: 10px; background: linear-gradient(135deg, #4f46e5, #7c3aed); font-size: 1rem; }

.st-key-hero {
  background: linear-gradient(135deg, #eef2ff 0%, #faf5ff 55%, #ecfeff 100%);
  border: 1px solid #e0e7ff; border-radius: 28px; padding: 3.2rem 2rem 2.2rem;
  text-align: center; margin-top: .8rem;
}
.badge { display: inline-block; padding: .35rem .9rem; border-radius: 999px; background: #fff; border: 1px solid #e0e7ff; color: var(--brand); font-weight: 600; font-size: .85rem; }
.hero-title { font-size: 3.1rem; line-height: 1.1; font-weight: 800; letter-spacing: -.03em; color: var(--ink); margin: 1rem auto .8rem; max-width: 820px; }
.grad { background: linear-gradient(90deg, #4f46e5, #7c3aed); -webkit-background-clip: text; background-clip: text; color: transparent; }
.lead { font-size: 1.15rem; color: #475569; max-width: 680px; margin: 0 auto 1.6rem; line-height: 1.6; }
.hero-note { color: var(--muted); font-size: .9rem; margin-top: .8rem; }

.mock-wrap { margin: 2.5rem auto 0; max-width: 780px; }
.mock-label { text-align: center; color: var(--muted); font-size: .85rem; margin-bottom: .6rem; }
.mock { box-shadow: 0 20px 50px rgba(79, 70, 229, .12); height: auto; }

.section { margin-top: 4.5rem; text-align: center; }
.section-title { font-size: 2rem; font-weight: 800; letter-spacing: -.02em; color: var(--ink); }
.section-sub { color: var(--muted); max-width: 640px; margin: .5rem auto 2rem; line-height: 1.6; }
.grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.2rem; text-align: left; }
.grid3 .card h4 { margin: 0 0 .35rem; font-size: 1.05rem; color: var(--ink); }
.grid3 .card p { margin: 0; color: #475569; line-height: 1.55; font-size: .95rem; }
.icon-tile { width: 46px; height: 46px; border-radius: 12px; display: grid; place-items: center; font-size: 1.4rem; margin-bottom: .8rem; background: #eef2ff; }
.step-n { width: 34px; height: 34px; border-radius: 50%; display: grid; place-items: center; background: linear-gradient(135deg, #4f46e5, #7c3aed); color: #fff; font-weight: 700; margin-bottom: .8rem; }

.st-key-cta_band {
  background: linear-gradient(135deg, #4f46e5, #7c3aed); border-radius: 28px;
  padding: 3rem 2rem 2.6rem; text-align: center; margin-top: 4.5rem;
}
.cta-title { color: #fff; font-size: 2rem; font-weight: 800; letter-spacing: -.02em; }
.cta-sub { color: #e0e7ff; margin: .4rem 0 1.4rem; }
.st-key-cta_final button { background: #fff; border: 0; }
.st-key-cta_final button p { color: #4f46e5; font-weight: 700; }

.footer { text-align: center; color: var(--muted); font-size: .9rem; margin: 3rem 0 1rem; }

@media (max-width: 820px) {
  .grid3 { grid-template-columns: 1fr; }
  .hero-title { font-size: 2.1rem; }
}
"""

DASH_CSS = """
.block-container { max-width: 1080px; padding-top: 1.6rem; }
.dash-title { font-size: 1.9rem; font-weight: 800; letter-spacing: -.02em; color: var(--ink); }
.dash-sub { color: var(--muted); margin-bottom: 1rem; }

section[data-testid="stSidebar"] { border-right: 1px solid var(--line); }
section[data-testid="stSidebar"][aria-expanded="true"] { min-width: 24rem; max-width: 32rem; }
.side-brand { font-weight: 800; font-size: 1.15rem; color: var(--ink); margin: .2rem 0 .8rem; }
.side-head { font-weight: 700; color: var(--ink); margin: 1rem 0 .3rem; font-size: .95rem; }
.file-row { padding: .45rem .6rem; border: 1px solid var(--line); border-radius: 10px; margin-bottom: .4rem; background: #fff; font-size: .85rem; color: var(--ink); }
.file-row small { display: block; color: var(--muted); }

.empty { text-align: center; color: var(--muted); padding: 2.6rem 1rem; border: 1px dashed #cbd5e1; border-radius: 18px; background: #fff; margin-top: 1rem; }
.empty b { color: var(--ink); display: block; font-size: 1.1rem; margin-bottom: .3rem; }

.ba { border: 1px solid var(--line); border-radius: 14px; padding: .9rem 1rem; line-height: 1.5; height: 100%; }
.ba-before { background: #f8fafc; color: #475569; }
.ba-after { background: #eef2ff; border-color: #c7d2fe; color: var(--ink); }
.ba-label { font-size: .72rem; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin-bottom: .3rem; }
.ba-why { color: var(--muted); font-size: .88rem; margin: .35rem 0 1rem; }
"""


def inject(page):
    css = COMMON_CSS + (DASH_CSS if page == "dashboard" else LANDING_CSS)
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)