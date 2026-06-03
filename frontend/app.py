import re
import time
import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
section.main {
    background: #0a0a0f !important;
    color: #e8eaf0 !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stDecoration"] { display: none !important; }
footer { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; }

[data-testid="stMainBlockContainer"] {
    padding: 1.5rem 2.5rem 2rem !important;
    max-width: 960px !important;
}

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #252535; border-radius: 3px; }

/* ══ SIDEBAR ══ */
section[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
    background: #0f0f1a !important;
    border-right: 1px solid #1a1a2e !important;
    min-width: 240px !important;
    width: 240px !important;
}
section[data-testid="stSidebar"] > div {
    padding: 1.1rem 0.9rem 1rem !important;
}

.sb-brand {
    display: flex; align-items: center; gap: 10px;
    padding-bottom: 0.9rem;
    border-bottom: 1px solid #1a1a2e;
    margin-bottom: 1rem;
}
.sb-brand-icon {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #10a37f, #0d7a5f);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    box-shadow: 0 0 14px rgba(16,163,127,0.3);
}
.sb-brand-name { font-size: 0.9rem; font-weight: 700; color: #fff; letter-spacing: -0.01em; }
.sb-brand-ver  { font-size: 0.6rem; color: #555; font-family:'JetBrains Mono',monospace; letter-spacing:0.08em; }

.sb-label {
    font-size: 0.6rem; font-family:'JetBrains Mono',monospace;
    color: #444; text-transform: uppercase; letter-spacing: 0.12em;
    margin: 0.5rem 0 0.35rem; padding: 0 2px;
}

.sb-yt [data-testid="stButton"] > button {
    background: rgba(239,68,68,0.07) !important;
    border: 1px solid rgba(239,68,68,0.18) !important;
    border-radius: 9px !important; color: #f87171 !important;
    font-family:'Inter',sans-serif !important; font-size:0.82rem !important;
    font-weight:500 !important; padding:0.52rem 0.9rem !important; width:100% !important;
    transition:all 0.2s !important; text-align:left !important;
}
.sb-yt [data-testid="stButton"] > button:hover {
    background:rgba(239,68,68,0.14) !important; border-color:rgba(239,68,68,0.35) !important;
    transform: translateX(2px) !important;
}
.sb-pdf [data-testid="stButton"] > button {
    background: rgba(59,130,246,0.07) !important;
    border: 1px solid rgba(59,130,246,0.18) !important;
    border-radius: 9px !important; color: #93c5fd !important;
    font-family:'Inter',sans-serif !important; font-size:0.82rem !important;
    font-weight:500 !important; padding:0.52rem 0.9rem !important; width:100% !important;
    transition:all 0.2s !important;
}
.sb-pdf [data-testid="stButton"] > button:hover {
    background:rgba(59,130,246,0.14) !important; border-color:rgba(59,130,246,0.35) !important;
    transform: translateX(2px) !important;
}
.sb-clr [data-testid="stButton"] > button {
    background: transparent !important; border: 1px solid #1a1a2e !important;
    border-radius: 9px !important; color: #444 !important;
    font-family:'Inter',sans-serif !important; font-size:0.8rem !important;
    font-weight:500 !important; padding:0.52rem 0.9rem !important; width:100% !important;
    transition:all 0.2s !important;
}
.sb-clr [data-testid="stButton"] > button:hover { border-color:#252535 !important; color:#888 !important; }

.status-online {
    display:flex; align-items:center; gap:7px;
    background: rgba(16,163,127,0.07);
    border: 1px solid rgba(16,163,127,0.16);
    border-radius: 8px; padding: 7px 11px;
    font-size: 0.7rem; color: #34d399;
    font-family:'JetBrains Mono',monospace; letter-spacing:0.04em;
    margin-top: 0.6rem;
}
.sdot { width:6px; height:6px; border-radius:50%; background:#34d399;
    box-shadow:0 0 7px #34d399; animation:blink 2s infinite; flex-shrink:0; }
@keyframes blink { 0%,100%{opacity:1;box-shadow:0 0 7px #34d399;} 50%{opacity:0.3;box-shadow:none;} }

.sb-hist-title {
    font-size:0.6rem; font-family:'JetBrains Mono',monospace;
    color:#333; text-transform:uppercase; letter-spacing:0.12em;
    margin: 0.8rem 0 0.3rem; padding: 0 2px;
}
.hist-chip {
    background:#111120; border:1px solid #1a1a2e; border-radius:7px;
    padding:5px 9px; margin-bottom:4px;
    font-size:0.72rem; color:#555; font-family:'JetBrains Mono',monospace;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
    transition: all 0.15s;
}
.hist-chip:hover { background:#161625; color:#888; border-color:#252535; }

/* ══ HOME ══ */
.home-hero { text-align: center; padding: 3.5rem 1rem 2.8rem; }
.home-tag {
    display: inline-block;
    background: rgba(16,163,127,0.1); border: 1px solid rgba(16,163,127,0.2);
    border-radius: 20px; color: #34d399; font-size: 0.68rem;
    font-family:'JetBrains Mono',monospace; letter-spacing: 0.1em;
    text-transform: uppercase; padding: 4px 14px; margin-bottom: 1rem;
}
.home-title { font-size: 2.4rem; font-weight: 700; color: #fff;
    letter-spacing: -0.04em; line-height: 1.1; margin-bottom: 0.6rem; }
.home-title em { color: #10a37f; font-style: normal; }
.home-sub { font-size: 0.8rem; color: #444;
    font-family:'JetBrains Mono',monospace; letter-spacing: 0.04em; }

.card { background: #0f0f1a; border-radius: 18px;
    padding: 1.8rem 1.5rem 1.4rem; position: relative; overflow: hidden; transition: all 0.28s; }
.card-yt  { border: 1px solid rgba(239,68,68,0.18); }
.card-pdf { border: 1px solid rgba(59,130,246,0.18); }
.card-yt:hover  { border-color:rgba(239,68,68,0.5); background:#160f0f;
    box-shadow:0 16px 40px rgba(239,68,68,0.1); transform:translateY(-3px); }
.card-pdf:hover { border-color:rgba(59,130,246,0.5); background:#0f1020;
    box-shadow:0 16px 40px rgba(59,130,246,0.1); transform:translateY(-3px); }
.card-yt::before  { content:''; position:absolute; top:-30px; right:-30px; width:110px; height:110px;
    border-radius:50%; background:radial-gradient(circle,rgba(239,68,68,0.1),transparent 70%); }
.card-pdf::before { content:''; position:absolute; top:-30px; right:-30px; width:110px; height:110px;
    border-radius:50%; background:radial-gradient(circle,rgba(59,130,246,0.1),transparent 70%); }
.card-icon { width:52px; height:52px; border-radius:14px;
    display:flex; align-items:center; justify-content:center; margin-bottom:1rem; }
.ci-yt  { background:linear-gradient(135deg,#b91c1c,#ef4444); box-shadow:0 4px 16px rgba(239,68,68,0.35); }
.ci-pdf { background:linear-gradient(135deg,#1d4ed8,#3b82f6); box-shadow:0 4px 16px rgba(59,130,246,0.35); }
.card-title { font-size:1.08rem; font-weight:700; color:#fff; margin-bottom:5px; }
.card-desc  { font-size:0.76rem; color:#444; line-height:1.6; margin-bottom:1.1rem; }

.cbtn-yt [data-testid="stButton"] > button {
    background:linear-gradient(135deg,#b91c1c,#ef4444) !important;
    border:none !important; border-radius:10px !important; color:#fff !important;
    font-family:'Inter',sans-serif !important; font-weight:600 !important;
    font-size:0.84rem !important; padding:0.5rem 1.1rem !important; width:100% !important;
    box-shadow:0 4px 16px rgba(239,68,68,0.3) !important; transition:all 0.22s !important;
}
.cbtn-yt [data-testid="stButton"] > button:hover { transform:translateY(-2px) !important; box-shadow:0 8px 22px rgba(239,68,68,0.45) !important; }
.cbtn-pdf [data-testid="stButton"] > button {
    background:linear-gradient(135deg,#1d4ed8,#3b82f6) !important;
    border:none !important; border-radius:10px !important; color:#fff !important;
    font-family:'Inter',sans-serif !important; font-weight:600 !important;
    font-size:0.84rem !important; padding:0.5rem 1.1rem !important; width:100% !important;
    box-shadow:0 4px 16px rgba(59,130,246,0.3) !important; transition:all 0.22s !important;
}
.cbtn-pdf [data-testid="stButton"] > button:hover { transform:translateY(-2px) !important; box-shadow:0 8px 22px rgba(59,130,246,0.45) !important; }

/* ══ CHAT HEADER ══ */
.chat-hdr { display:flex; align-items:center; gap:11px;
    padding:0.8rem 0; border-bottom:1px solid #141420; margin-bottom:0.7rem; }
.chat-hdr-icon { width:38px; height:38px; border-radius:10px;
    display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.hi-yt  { background:linear-gradient(135deg,#b91c1c,#ef4444); box-shadow:0 3px 12px rgba(239,68,68,0.4); }
.hi-pdf { background:linear-gradient(135deg,#1d4ed8,#3b82f6); box-shadow:0 3px 12px rgba(59,130,246,0.4); }
.chat-hdr-title { font-size:1rem; font-weight:700; color:#fff; }
.chat-hdr-sub   { font-size:0.66rem; color:#444; font-family:'JetBrains Mono',monospace;
    letter-spacing:0.04em; margin-top:1px; }

.btn-back [data-testid="stButton"] > button,
.btn-sm   [data-testid="stButton"] > button {
    background:#0f0f1a !important; border:1px solid #1a1a2e !important;
    border-radius:8px !important; color:#444 !important;
    font-family:'Inter',sans-serif !important; font-size:0.75rem !important;
    font-weight:500 !important; padding:0.34rem 0.8rem !important;
    width:auto !important; transition:all 0.18s !important;
}
.btn-back [data-testid="stButton"] > button:hover,
.btn-sm   [data-testid="stButton"] > button:hover {
    background:#141420 !important; color:#bbb !important; border-color:#252535 !important; }

/* ══ INPUTS ══ */
[data-testid="stTextInput"] > div > div {
    background:#0f0f1a !important; border:1px solid #1a1a2e !important; border-radius:10px !important; }
[data-testid="stTextInput"] input {
    background:transparent !important; color:#e8eaf0 !important;
    font-family:'Inter',sans-serif !important; font-size:0.88rem !important; }
[data-testid="stTextInput"] input:focus { box-shadow:0 0 0 2px rgba(16,163,127,0.25) !important; }
[data-testid="stTextInput"] label {
    color:#555 !important; font-size:0.68rem !important;
    font-family:'JetBrains Mono',monospace !important; text-transform:uppercase !important; letter-spacing:0.08em !important; }

[data-testid="stSelectbox"] > div > div {
    background:#0f0f1a !important; border:1px solid #1a1a2e !important; border-radius:10px !important; color:#e8eaf0 !important; }
[data-testid="stSelectbox"] label {
    color:#555 !important; font-size:0.68rem !important;
    font-family:'JetBrains Mono',monospace !important; text-transform:uppercase !important; letter-spacing:0.08em !important; }
[data-testid="stSelectbox"] svg { color:#444 !important; }

[data-testid="stFileUploader"] {
    background:#0f0f1a !important; border:1.5px dashed #1a1a2e !important; border-radius:10px !important; }
[data-testid="stFileUploader"] label {
    color:#555 !important; font-size:0.68rem !important;
    font-family:'JetBrains Mono',monospace !important; text-transform:uppercase !important; }

[data-testid="stChatInput"] {
    background:#0f0f1a !important; border:1px solid #1a1a2e !important; border-radius:14px !important; }
[data-testid="stChatInput"] textarea {
    background:transparent !important; color:#e8eaf0 !important;
    font-family:'Inter',sans-serif !important; font-size:0.88rem !important; }
[data-testid="stChatInput"]:focus-within { border-color:#10a37f !important; box-shadow:0 0 0 2px rgba(16,163,127,0.15) !important; }
[data-testid="stChatInput"] button { background:#10a37f !important; border-radius:9px !important; }

/* ══ SUGGESTION TOGGLE ══ */
.sugg-tog [data-testid="stButton"] > button {
    background:#0f0f1a !important; border:1px solid #1a1a2e !important;
    border-radius:10px !important; color:#555 !important;
    font-family:'Inter',sans-serif !important; font-size:0.8rem !important;
    font-weight:500 !important; padding:0.44rem 0.7rem !important;
    width:100% !important; transition:all 0.18s !important;
}
.sugg-tog [data-testid="stButton"] > button:hover { background:#141420 !important; color:#aaa !important; border-color:#252535 !important; }
.sugg-tog-on [data-testid="stButton"] > button {
    background:rgba(16,163,127,0.1) !important;
    border:1px solid rgba(16,163,127,0.3) !important; color:#34d399 !important; }

/* ══ SUGGESTION PANEL ══ */
.sugg-panel {
    background:#0c0c18; border:1px solid #151525; border-radius:13px;
    padding:0.9rem 1rem 0.6rem; margin-bottom:0.6rem; animation:fadein 0.22s ease; }
@keyframes fadein { from{opacity:0;transform:translateY(-5px);} to{opacity:1;transform:translateY(0);} }
.sugg-panel-hdr { font-size:0.62rem; color:#444; font-family:'JetBrains Mono',monospace;
    text-transform:uppercase; letter-spacing:0.12em; margin-bottom:0.55rem; }
.sc [data-testid="stButton"] > button {
    background:#0f0f1a !important; border:1px solid #1a1a2e !important;
    border-radius:9px !important; color:#666 !important;
    font-family:'Inter',sans-serif !important; font-size:0.76rem !important;
    font-weight:500 !important; padding:0.42rem 0.7rem !important; width:100% !important;
    text-align:left !important; transition:all 0.15s !important; }
.sc [data-testid="stButton"] > button:hover { background:#141420 !important; color:#bbb !important; border-color:#252535 !important; }

/* ══ PROFESSIONAL ANSWER CARD ══ */
.answer-card {
    background: #0f0f1a;
    border: 1px solid #1a1a2e;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.88rem;
    line-height: 1.75;
    color: #d4d8e8;
}
/* Bold label rows like "Definition:", "Why needed:" */
.answer-card .label-row {
    display: flex;
    gap: 8px;
    margin-bottom: 6px;
    align-items: flex-start;
}
.answer-card .label-key {
    color: #60a5fa;
    font-weight: 600;
    font-size: 0.84rem;
    white-space: nowrap;
    min-width: fit-content;
}
.answer-card .label-val {
    color: #c9cde0;
    font-size: 0.86rem;
}
/* Bullet point rows */
.answer-card .bullet-row {
    display: flex;
    gap: 10px;
    margin-bottom: 5px;
    align-items: flex-start;
}
.answer-card .bullet-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #10a37f;
    flex-shrink: 0;
    margin-top: 7px;
}
.answer-card .bullet-text {
    color: #c9cde0;
    font-size: 0.86rem;
    line-height: 1.65;
}
/* Plain single-sentence answer */
.answer-card .plain-text {
    color: #d4d8e8;
    font-size: 0.88rem;
}

/* ══ THINKING ANIMATION ══ */
.thinking {
    display:inline-flex; align-items:center; gap:10px;
    background:#0f0f1a; border:1px solid #1a1a2e;
    border-radius:12px; padding:10px 16px; margin:4px 0;
}
.tdots { display:flex; gap:5px; align-items:center; }
.tdots span { width:7px; height:7px; border-radius:50%; background:#10a37f;
    animation:tbounce 1.3s infinite ease-in-out; }
.tdots span:nth-child(1){animation-delay:0s;}
.tdots span:nth-child(2){animation-delay:0.18s;}
.tdots span:nth-child(3){animation-delay:0.36s;}
@keyframes tbounce { 0%,60%,100%{transform:translateY(0);opacity:0.35;} 30%{transform:translateY(-6px);opacity:1;} }
.ttext { font-size:0.76rem; color:#444; font-family:'JetBrains Mono',monospace;
    letter-spacing:0.03em; animation:tpulse 1.6s infinite; }
@keyframes tpulse { 0%,100%{opacity:0.4;} 50%{opacity:1;} }

/* ══ SOURCE EXPANDER ══ */
[data-testid="stExpander"] {
    background:#0c0c18 !important; border:1px solid #151525 !important; border-radius:10px !important; }
[data-testid="stExpander"] summary { color:#444 !important; font-size:0.73rem !important; font-family:'JetBrains Mono',monospace !important; }

div[data-testid="stAlert"] { background:#0a1a0f !important; border:1px solid #163a1f !important; border-radius:10px !important; }
hr { border-color:#141420 !important; margin:0.6rem 0 !important; }
[data-testid="stSpinner"] { color:#10a37f !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════
for k, v in {
    "chat_history": [], "mode": None, "stored_pdf": None,
    "show_suggestions": False, "pending_query": None,
    "yt_history": [], "pdf_history": [],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════
# ANSWER RENDERER — professional structured output
# ══════════════════════════════════════════════════════════════════

def render_answer_html(lines: list[str]) -> str:
    """
    Convert backend answer lines into a professional styled HTML card.
    Handles three formats:
      1. Bold labels  → **Definition:** some text
      2. Bullet lines → - some text  OR  • some text
      3. Plain text   → single sentence answer
    """
    import html as html_lib

    rows_html = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # ── Format 1: Bold label like **Definition:** text ──
        label_match = re.match(r"^\*\*(.+?):\*\*\s*(.*)", line)
        if label_match:
            key  = html_lib.escape(label_match.group(1))
            val  = html_lib.escape(label_match.group(2).strip())
            rows_html.append(
                f'<div class="label-row">'
                f'<span class="label-key">{key}:</span>'
                f'<span class="label-val">{val}</span>'
                f'</div>'
            )
            continue

        # ── Format 2: Bullet line starting with - or • ──
        bullet_match = re.match(r"^[-•]\s+(.*)", line)
        if bullet_match:
            text = html_lib.escape(bullet_match.group(1).strip())
            rows_html.append(
                f'<div class="bullet-row">'
                f'<span class="bullet-dot"></span>'
                f'<span class="bullet-text">{text}</span>'
                f'</div>'
            )
            continue

        # ── Format 3: Plain sentence ──
        rows_html.append(
            f'<div class="plain-text">{html_lib.escape(line)}</div>'
        )

    if not rows_html:
        return '<div class="plain-text">No answer found.</div>'

    return (
        '<div class="answer-card">'
        + "".join(rows_html)
        + '</div>'
    )


def stream_and_render(answer_lines: list[str]) -> str:
    """
    Show a typing effect line-by-line, then replace with the
    fully rendered professional HTML card.
    """
    placeholder = st.empty()

    # ── Step 1: stream raw text so user sees something immediately ──
    streamed = ""
    for line in answer_lines:
        line = line.strip()
        if not line:
            continue
        # strip markdown bold markers for the streaming preview
        preview = re.sub(r"\*\*(.+?):\*\*", r"\1:", line)
        preview = re.sub(r"^[-•]\s+", "• ", preview)
        temp = ""
        for word in preview.split():
            temp += word + " "
            placeholder.markdown(streamed + temp)
            time.sleep(0.012)
        streamed += preview + "\n\n"
        placeholder.markdown(streamed)

    # ── Step 2: replace with rich HTML card ──
    final_html = render_answer_html(answer_lines)
    placeholder.markdown(final_html, unsafe_allow_html=True)

    # Return plain text version for chat history storage
    plain = "\n\n".join(
        re.sub(r"\*\*(.+?):\*\*", r"**\1:**", l.strip())
        for l in answer_lines if l.strip()
    )
    return plain


def show_sources(sources):
    if not sources:
        return
    with st.expander("📎 View Source Chunks"):
        for i, src in enumerate(sources[:3]):
            st.markdown(
                f'<div style="background:#0c0c18;padding:11px 13px;border-radius:9px;'
                f'border-left:3px solid #6366f1;margin-bottom:10px;'
                f'font-size:0.76rem;color:#777;font-family:JetBrains Mono,monospace;'
                f'line-height:1.65;">'
                f'<span style="color:#3a3a5a;font-size:0.62rem;text-transform:uppercase;'
                f'letter-spacing:0.08em;">Chunk {i+1}</span><br><br>'
                f'{src[:400]}</div>',
                unsafe_allow_html=True
            )


def add_to_yt_history(vid):
    if vid and vid.strip() and vid.strip() not in st.session_state.yt_history:
        st.session_state.yt_history.insert(0, vid.strip())
        st.session_state.yt_history = st.session_state.yt_history[:5]

def add_to_pdf_history(name):
    if name and name not in st.session_state.pdf_history:
        st.session_state.pdf_history.insert(0, name)
        st.session_state.pdf_history = st.session_state.pdf_history[:5]

SUGGESTIONS = {
    "youtube": [
        "📝  Summarize this video",
        "🔑  What are the key points?",
        "💡  Explain the main idea",
        "📋  List all topics covered",
        "🎯  What is the conclusion?",
        "❓  What questions does this answer?",
    ],
    "pdf": [
        "📝  Summarize this document",
        "🔑  What are the key points?",
        "💡  Explain the main concept",
        "📋  List all topics covered",
        "🎯  What is the conclusion?",
        "🔍  What are the important definitions?",
    ]
}

def render_sugg_panel(mode):
    if not st.session_state.show_suggestions:
        return
    st.markdown('<div class="sugg-panel"><div class="sugg-panel-hdr">💡 Suggested Questions</div></div>', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, chip in enumerate(SUGGESTIONS[mode]):
        with cols[i % 2]:
            st.markdown('<div class="sc">', unsafe_allow_html=True)
            if st.button(chip, key=f"chip_{mode}_{i}"):
                clean = chip.split("  ", 1)[-1] if "  " in chip else chip
                st.session_state.pending_query = clean
                st.session_state.show_suggestions = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

THINKING_HTML = """<div class="thinking">
  <div class="tdots"><span></span><span></span><span></span></div>
  <div class="ttext">{msg}</div>
</div>"""

# ══════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
      <div class="sb-brand-icon">🤖</div>
      <div>
        <div class="sb-brand-name">AI Assistant</div>
        <div class="sb-brand-ver">MULTI-SOURCE · v2.0</div>
      </div>
    </div>
    <div class="sb-label">Chat Modes</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-yt">', unsafe_allow_html=True)
    if st.button("▶  YouTube Chat", key="sb_yt"):
        st.session_state.mode = "youtube"
        st.session_state.chat_history = []
        st.session_state.show_suggestions = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-pdf" style="margin-top:5px;">', unsafe_allow_html=True)
    if st.button("📄  PDF Chat", key="sb_pdf"):
        st.session_state.mode = "pdf"
        st.session_state.chat_history = []
        st.session_state.show_suggestions = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#141420;margin:0.9rem 0;'>", unsafe_allow_html=True)

    st.markdown('<div class="sb-clr">', unsafe_allow_html=True)
    if st.button("🧹  Clear Chat", key="sb_clear"):
        st.session_state.chat_history = []
        st.session_state.show_suggestions = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="status-online"><span class="sdot"></span>System Online</div>', unsafe_allow_html=True)

    if st.session_state.yt_history:
        st.markdown('<div class="sb-hist-title">▶ Recent Videos</div>', unsafe_allow_html=True)
        for vid in st.session_state.yt_history:
            st.markdown(f'<div class="hist-chip">{vid}</div>', unsafe_allow_html=True)

    if st.session_state.pdf_history:
        st.markdown('<div class="sb-hist-title">📄 Recent PDFs</div>', unsafe_allow_html=True)
        for pdf in st.session_state.pdf_history:
            label = pdf if len(pdf) <= 24 else pdf[:21] + "…"
            st.markdown(f'<div class="hist-chip">{label}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════════════
if st.session_state.mode is None:

    st.markdown("""
    <div class="home-hero">
      <div class="home-tag">AI · RAG · LangChain · Groq</div>
      <div class="home-title">Multi-Source <em>AI</em> Chatbot</div>
      <div class="home-sub">Chat with YouTube videos &amp; PDF documents using AI</div>
    </div>
    """, unsafe_allow_html=True)

    c1, gap, c2 = st.columns([1, 0.08, 1])

    with c1:
        st.markdown("""
        <div class="card card-yt">
          <div class="card-icon ci-yt">
            <svg width="26" height="18" viewBox="0 0 26 18" fill="none">
              <path d="M25.44 2.82C25.13 1.68 24.24.79 23.1.48 21.09 0 13 0 13 0S4.91 0 2.9.48C1.76.79.87 1.68.56 2.82.08 4.84.08 9 .08 9S.08 13.16.56 15.18C.87 16.32 1.76 17.21 2.9 17.52 4.91 18 13 18 13 18S21.09 18 23.1 17.52C24.24 17.21 25.13 16.32 25.44 15.18 25.92 13.16 25.92 9 25.92 9S25.92 4.84 25.44 2.82Z" fill="white"/>
              <path d="M10.4 12.82L17.14 9 10.4 5.18V12.82Z" fill="#EF4444"/>
            </svg>
          </div>
          <div class="card-title">YouTube Chatbot</div>
          <div class="card-desc">Paste any YouTube Video ID and have an intelligent conversation with the full video transcript using RAG.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="cbtn-yt" style="margin-top:10px;">', unsafe_allow_html=True)
        if st.button("▶  Start YouTube Chat", key="home_yt"):
            st.session_state.mode = "youtube"
            st.session_state.chat_history = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card card-pdf">
          <div class="card-icon ci-pdf">
            <svg width="22" height="26" viewBox="0 0 24 28" fill="none">
              <path d="M14 0H2C.9 0 0 .9 0 2V26C0 27.1.9 28 2 28H22C23.1 28 24 27.1 24 26V10L14 0Z" fill="white" opacity=".92"/>
              <path d="M14 0V10H24L14 0Z" fill="#93c5fd"/>
              <rect x="4" y="14" width="16" height="1.5" rx=".75" fill="#1d4ed8"/>
              <rect x="4" y="18" width="12" height="1.5" rx=".75" fill="#1d4ed8"/>
              <rect x="4" y="22" width="14" height="1.5" rx=".75" fill="#1d4ed8"/>
            </svg>
          </div>
          <div class="card-title">PDF Chatbot</div>
          <div class="card-desc">Upload any PDF document and instantly ask questions, get summaries and extract key information.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="cbtn-pdf" style="margin-top:10px;">', unsafe_allow_html=True)
        if st.button("📄  Start PDF Chat", key="home_pdf"):
            st.session_state.mode = "pdf"
            st.session_state.chat_history = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE: YOUTUBE CHAT
# ══════════════════════════════════════════════════════════════════
elif st.session_state.mode == "youtube":

    hc1, hc2 = st.columns([6, 1])
    with hc1:
        st.markdown("""
        <div class="chat-hdr">
          <div class="chat-hdr-icon hi-yt">
            <svg width="20" height="14" viewBox="0 0 26 18" fill="none">
              <path d="M25.44 2.82C25.13 1.68 24.24.79 23.1.48 21.09 0 13 0 13 0S4.91 0 2.9.48C1.76.79.87 1.68.56 2.82.08 4.84.08 9 .08 9S.08 13.16.56 15.18C.87 16.32 1.76 17.21 2.9 17.52 4.91 18 13 18 13 18S21.09 18 23.1 17.52C24.24 17.21 25.13 16.32 25.44 15.18 25.92 13.16 25.92 9 25.92 9S25.92 4.84 25.44 2.82Z" fill="white"/>
              <path d="M10.4 12.82L17.14 9 10.4 5.18V12.82Z" fill="#EF4444"/>
            </svg>
          </div>
          <div class="chat-hdr-info">
            <div class="chat-hdr-title">YouTube Chatbot</div>
            <div class="chat-hdr-sub">chat with any youtube video transcript</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with hc2:
        st.markdown('<div class="btn-back" style="padding-top:14px;">', unsafe_allow_html=True)
        if st.button("← Home", key="yt_back"):
            st.session_state.mode = None
            st.session_state.chat_history = []
            st.session_state.show_suggestions = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    vc1, vc2, vc3 = st.columns([3, 2, 1])
    with vc1:
        video_id = st.text_input("Enter Video ID", placeholder="e.g. dQw4w9WgXcQ", key="yt_vid")
    with vc2:
        hist_opts = ["— select recent —"] + st.session_state.yt_history
        hist_choice = st.selectbox("Recent Video IDs", hist_opts, key="yt_hist_sel")
        if hist_choice != "— select recent —":
            video_id = hist_choice
    with vc3:
        st.markdown('<div class="btn-sm" style="padding-top:22px;">', unsafe_allow_html=True)
        if st.button("🧹 Clear", key="yt_clear"):
            st.session_state.chat_history = []
            st.session_state.show_suggestions = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    render_sugg_panel("youtube")

    inp_col, btn_col = st.columns([9, 1])
    with inp_col:
        query = st.chat_input("Ask about the video…")
    with btn_col:
        lbl = "💡✕" if st.session_state.show_suggestions else "💡"
        css = "sugg-tog-on" if st.session_state.show_suggestions else "sugg-tog"
        st.markdown(f'<div class="{css}" style="padding-top:4px;">', unsafe_allow_html=True)
        if st.button(lbl, key="yt_sugg_tog"):
            st.session_state.show_suggestions = not st.session_state.show_suggestions
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.pending_query:
        query = st.session_state.pending_query
        st.session_state.pending_query = None

    if query:
        add_to_yt_history(video_id)
        st.session_state.chat_history.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        with st.chat_message("assistant"):
            tp = st.empty()
            tp.markdown(THINKING_HTML.format(msg="Thinking…"), unsafe_allow_html=True)
            try:
                res = requests.post(
                    f"{BACKEND_URL}/chat/youtube",
                    json={"video_id": video_id, "question": query,
                          "chat_history": str(st.session_state.chat_history)}
                )
                tp.empty()
                data = res.json()
                answer  = data.get("answer", [])
                sources = data.get("sources", [])
                final_text = stream_and_render(answer)
                st.session_state.chat_history.append({"role": "assistant", "content": final_text})
                show_sources(sources)
            except Exception as e:
                tp.empty()
                st.error(str(e))

# ══════════════════════════════════════════════════════════════════
# PAGE: PDF CHAT
# ══════════════════════════════════════════════════════════════════
elif st.session_state.mode == "pdf":

    hc1, hc2 = st.columns([6, 1])
    with hc1:
        st.markdown("""
        <div class="chat-hdr">
          <div class="chat-hdr-icon hi-pdf">
            <svg width="18" height="22" viewBox="0 0 24 28" fill="none">
              <path d="M14 0H2C.9 0 0 .9 0 2V26C0 27.1.9 28 2 28H22C23.1 28 24 27.1 24 26V10L14 0Z" fill="white" opacity=".92"/>
              <path d="M14 0V10H24L14 0Z" fill="#93c5fd"/>
              <rect x="3" y="14" width="13" height="1.5" rx=".75" fill="#1d4ed8"/>
              <rect x="3" y="18" width="10" height="1.5" rx=".75" fill="#1d4ed8"/>
              <rect x="3" y="22" width="11" height="1.5" rx=".75" fill="#1d4ed8"/>
            </svg>
          </div>
          <div class="chat-hdr-info">
            <div class="chat-hdr-title">PDF Chatbot</div>
            <div class="chat-hdr-sub">upload a pdf and ask anything about it</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with hc2:
        st.markdown('<div class="btn-back" style="padding-top:14px;">', unsafe_allow_html=True)
        if st.button("← Home", key="pdf_back"):
            st.session_state.mode = None
            st.session_state.chat_history = []
            st.session_state.stored_pdf = None
            st.session_state.show_suggestions = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    uc1, uc2, uc3 = st.columns([3, 2, 1])
    with uc1:
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], key="pdf_uploader")
        if uploaded_file is not None:
            st.session_state.stored_pdf = uploaded_file
            add_to_pdf_history(uploaded_file.name)
        if st.session_state.stored_pdf is not None:
            uploaded_file = st.session_state.stored_pdf
            st.success(f"📄 {uploaded_file.name}")
    with uc2:
        pdf_opts = ["— select recent —"] + st.session_state.pdf_history
        pdf_sel = st.selectbox("Recent PDFs", pdf_opts, key="pdf_hist_sel")
        if pdf_sel != "— select recent —":
            st.markdown(
                f'<div style="font-size:0.7rem;color:#444;font-family:JetBrains Mono,monospace;'
                f'margin-top:3px;">↑ last used</div>',
                unsafe_allow_html=True
            )
    with uc3:
        st.markdown('<div class="btn-sm" style="padding-top:22px;">', unsafe_allow_html=True)
        if st.button("🧹 Clear", key="pdf_clear"):
            st.session_state.chat_history = []
            st.session_state.show_suggestions = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    render_sugg_panel("pdf")

    inp_col, btn_col = st.columns([9, 1])
    with inp_col:
        query = st.chat_input("Ask about the PDF…")
    with btn_col:
        lbl = "💡✕" if st.session_state.show_suggestions else "💡"
        css = "sugg-tog-on" if st.session_state.show_suggestions else "sugg-tog"
        st.markdown(f'<div class="{css}" style="padding-top:4px;">', unsafe_allow_html=True)
        if st.button(lbl, key="pdf_sugg_tog"):
            st.session_state.show_suggestions = not st.session_state.show_suggestions
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.pending_query:
        query = st.session_state.pending_query
        st.session_state.pending_query = None

    if query:
        if uploaded_file is None:
            st.warning("⚠️ Please upload a PDF first.")
        else:
            st.session_state.chat_history.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)
            with st.chat_message("assistant"):
                tp = st.empty()
                tp.markdown(THINKING_HTML.format(msg="Reading document…"), unsafe_allow_html=True)
                try:
                    res = requests.post(
                        f"{BACKEND_URL}/chat/pdf",
                        files={"file": (uploaded_file.name, uploaded_file, "application/pdf")},
                        data={"question": query, "chat_history": str(st.session_state.chat_history)}
                    )
                    tp.empty()
                    data = res.json()
                    answer  = data.get("answer", [])
                    sources = data.get("sources", [])
                    final_text = stream_and_render(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": final_text})
                    show_sources(sources)
                except Exception as e:
                    tp.empty()
                    st.error(str(e))