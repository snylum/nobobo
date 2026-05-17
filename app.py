import streamlit as st
from groq import Groq

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NOBOBO – Know Before You Vote",
    page_icon="🗳️",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

/* Reset & base */
html, body, [data-testid="stAppViewContainer"] {
    background: #0d0d0d;
    color: #f0ede6;
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stAppViewContainer"] { padding: 0; }
[data-testid="stHeader"] { display: none; }
#MainMenu, footer { display: none; }
[data-testid="stSidebar"] { display: none; }

/* ── NAV ── */
.nobobo-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 48px;
    background: #0d0d0d;
    border-bottom: 1px solid #222;
    position: sticky;
    top: 0;
    z-index: 100;
}
.nobobo-wordmark {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: #f0ede6;
    letter-spacing: -0.5px;
}
.nobobo-wordmark span { color: #e8ff5a; }
.nav-links {
    display: flex;
    align-items: center;
    gap: 8px;
}
.nav-link {
    color: #aaa;
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    border: none;
    background: transparent;
    transition: color 0.2s;
}
.nav-link:hover { color: #f0ede6; }
.nav-btn-chat {
    background: #e8ff5a;
    color: #0d0d0d !important;
    font-weight: 700;
    padding: 9px 20px;
    border-radius: 10px;
    font-size: 0.9rem;
    border: none;
    cursor: pointer;
    text-decoration: none;
}
.nav-btn-chat:hover { background: #d4eb40; }

/* ── HERO ── */
.hero {
    padding: 90px 48px 60px;
    max-width: 760px;
    margin: 0 auto;
    text-align: center;
}
.hero-tag {
    display: inline-block;
    background: #1a1a1a;
    border: 1px solid #333;
    color: #e8ff5a;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 6px 14px;
    border-radius: 100px;
    margin-bottom: 28px;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 4.5rem);
    font-weight: 800;
    line-height: 1.05;
    margin: 0 0 20px;
    letter-spacing: -1.5px;
}
.hero h1 em {
    font-style: normal;
    color: #e8ff5a;
}
.hero p {
    color: #888;
    font-size: 1.1rem;
    line-height: 1.7;
    max-width: 520px;
    margin: 0 auto 36px;
}

/* ── CHAT AREA ── */
.chat-wrap {
    max-width: 720px;
    margin: 0 auto;
    padding: 0 24px 80px;
}
.chat-bubble-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 12px;
}
.chat-bubble-user .bubble {
    background: #e8ff5a;
    color: #0d0d0d;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    max-width: 75%;
    font-size: 0.95rem;
    font-weight: 500;
    line-height: 1.5;
}
.chat-bubble-bot {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 12px;
}
.chat-bubble-bot .bubble {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    color: #f0ede6;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    max-width: 80%;
    font-size: 0.95rem;
    line-height: 1.65;
}
.bot-label {
    font-size: 0.7rem;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
    margin-left: 4px;
}

/* ── SECTION CARDS ── */
.section-wrap {
    max-width: 760px;
    margin: 0 auto;
    padding: 0 24px 80px;
}
.section-card {
    background: #141414;
    border: 1px solid #222;
    border-radius: 16px;
    padding: 36px;
    margin-bottom: 20px;
}
.section-card h2 {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    margin: 0 0 12px;
    color: #f0ede6;
}
.section-card p, .section-card li {
    color: #888;
    font-size: 0.95rem;
    line-height: 1.7;
}
.section-card ul { padding-left: 20px; }
.accent { color: #e8ff5a; }

/* Input overrides */
[data-testid="stTextInput"] input {
    background: #1a1a1a !important;
    border: 1px solid #333 !important;
    border-radius: 12px !important;
    color: #f0ede6 !important;
    padding: 14px 18px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #e8ff5a !important;
    box-shadow: 0 0 0 2px rgba(232,255,90,0.15) !important;
}
[data-testid="stButton"] button {
    background: #e8ff5a !important;
    color: #0d0d0d !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-size: 0.95rem !important;
    width: 100%;
}
[data-testid="stButton"] button:hover {
    background: #d4eb40 !important;
}
</style>
""", unsafe_allow_html=True)

# ── POLITICIAN DATA ───────────────────────────────────────────────────────────
# Paste your dataset here between the triple quotes.
# Example format shown below — replace with your real data.
POLITICIAN_DATA = """
POLITICIAN DATABASE (Philippines):

[PASTE YOUR DATA HERE]

Example entries:
- Name: Juan dela Cruz | Position: Senator | Party: Partido ng Bayan | Term: 2022-2028 | Contributions: Authored the Free Internet Access Act, Championed anti-corruption bills | Donations/Contributions received: ₱5M from XYZ Corp | Public info: Known for fiscal transparency

- Name: Maria Santos | Position: Representative, 1st District of Manila | Party: Liberal Party | Term: 2019-2025 | Contributions: Led housing reform bills, Climate change advocacy | Donations/Contributions received: None disclosed | Public info: Former human rights lawyer
"""

SYSTEM_PROMPT = f"""You are NOBOBO, a helpful and neutral AI assistant for Filipino voters.
Your job is to help people learn about Philippine politicians and candidates based only on the data provided below.

Rules:
- Only answer based on the data below. Do not make up information.
- If a politician is not in the data, say "I don't have data on that person yet."
- Be factual, neutral, and easy to understand.
- Keep answers concise but complete.
- You may answer in Filipino or English depending on how the user writes to you.
- Never express personal political opinions or endorse anyone.

POLITICIAN DATA:
{POLITICIAN_DATA}
"""

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── NAV ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nobobo-nav">
    <div class="nobobo-wordmark">NOBO<span>BO</span></div>
    <div class="nav-links" id="nav-links"></div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([6, 1, 1, 1.4])
with col2:
    if st.button("Home"):
        st.session_state.page = "home"
        st.rerun()
with col3:
    if st.button("About"):
        st.session_state.page = "about"
        st.rerun()
with col4:
    if st.button("💬 Chatbot"):
        st.session_state.page = "chat"
        st.rerun()

# ── PAGES ─────────────────────────────────────────────────────────────────────

# HOME PAGE
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero">
        <div class="hero-tag">🗳️ Philippine Elections</div>
        <h1>Know Before<br><em>You Vote</em></h1>
        <p>Ask NOBOBO anything about your candidates — their records,
        contributions, and public information. Make an informed vote.</p>
    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 2, 1])
    with center:
        if st.button("💬 Ask the Chatbot →"):
            st.session_state.page = "chat"
            st.rerun()

    st.markdown("""
    <div class="section-wrap">
        <div class="section-card">
            <h2>What can I ask?</h2>
            <ul>
                <li>Who is <span class="accent">[candidate name]</span>?</li>
                <li>What bills has <span class="accent">[senator]</span> authored?</li>
                <li>What party does <span class="accent">[candidate]</span> belong to?</li>
                <li>What are <span class="accent">[candidate]</span>'s contributions?</li>
                <li>Who funded <span class="accent">[candidate]</span>'s campaign?</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ABOUT PAGE
elif st.session_state.page == "about":
    st.markdown("""
    <div class="section-wrap" style="padding-top:48px;">
        <div class="section-card">
            <h2>About NOBOBO</h2>
            <p><span class="accent">NOBOBO</span> (Know Before You Vote) is a free, non-partisan
            tool that helps Filipino voters quickly access public information about candidates
            and elected officials.</p>
            <p style="margin-top:12px;">We believe every voter deserves easy access to facts —
            not spin. This chatbot is powered by a curated dataset of publicly available
            information on Philippine politicians.</p>
        </div>
        <div class="section-card">
            <h2>Data Sources</h2>
            <p>Our data is sourced from:</p>
            <ul>
                <li>Official COMELEC filings</li>
                <li>Senate and House of Representatives records</li>
                <li>Statement of Assets, Liabilities and Net Worth (SALN)</li>
                <li>Publicly available news and official statements</li>
            </ul>
            <p style="margin-top:12px;">We do not editorialize. All information is presented as filed or reported.</p>
        </div>
        <div class="section-card">
            <h2>Disclaimer</h2>
            <p>NOBOBO is an independent civic tool. It is not affiliated with any political
            party, candidate, or government agency. The AI may make mistakes — always
            verify important information through official sources.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# CHAT PAGE
elif st.session_state.page == "chat":
    st.markdown("""
    <div class="hero" style="padding-bottom:32px;">
        <div class="hero-tag">💬 AI Chatbot</div>
        <h1 style="font-size:2.8rem;">Ask <em>Anything</em></h1>
        <p>Type a candidate's name or ask about their record.</p>
    </div>
    """, unsafe_allow_html=True)

    # Chat history display
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-bubble-user">
                <div class="bubble">{msg["content"]}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-bubble-bot">
                <div>
                    <div class="bot-label">NOBOBO</div>
                    <div class="bubble">{msg["content"]}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Input
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="Ask about a candidate...", label_visibility="collapsed")
    send = st.button("Send →")
    st.markdown('</div>', unsafe_allow_html=True)

    if send and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *st.session_state.messages
                ],
                max_tokens=1024,
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = "⚠️ Sorry, I couldn't reach the AI right now. Please try again in a moment."

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.session_state.messages:
        if st.button("Clear chat"):
            st.session_state.messages = []
            st.rerun()
