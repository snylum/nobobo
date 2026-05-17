import streamlit as st
from groq import Groq
from pathlib import Path

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NOBOBO – Know Before You Vote",
    page_icon="🗳️",
    layout="centered",
)

# ── Load politician data from /data folder ────────────────────────────────────
def load_politician_data():
    """
    Walks the /data folder and reads all .txt files.
    Folder structure:
      data/
        ELEKSYON 2028/
          Presidential Candidates/
            DUTERTE.txt
            MARCOS.txt
          Vice Presidential Candidates/
            SARA.txt
    Returns a formatted string with all data labelled by election > category > name.
    """
    data_path = Path("data")
    all_data = []

    if not data_path.exists():
        return "No politician data loaded yet."

    for election_folder in sorted(data_path.iterdir()):
        if not election_folder.is_dir():
            continue
        all_data.append(f"\n{'='*40}")
        all_data.append(f"ELECTION: {election_folder.name}")
        all_data.append(f"{'='*40}")

        for category_folder in sorted(election_folder.iterdir()):
            if not category_folder.is_dir():
                continue
            all_data.append(f"\n  CATEGORY: {category_folder.name}")
            all_data.append(f"  {'-'*30}")

            for txt_file in sorted(category_folder.glob("*.txt")):
                name = txt_file.stem  # filename without .txt
                content = txt_file.read_text(encoding="utf-8").strip()
                all_data.append(f"\n  CANDIDATE: {name}")
                all_data.append(f"  {content}")

    return "\n".join(all_data) if all_data else "No politician data loaded yet."


POLITICIAN_DATA = load_politician_data()

SYSTEM_PROMPT = f"""You are NOBOBO, a helpful and strictly neutral AI chatbot for Filipino voters.
Your only job is to share factual information about Philippine politicians from the database below.

STRICT RULES:
- Only use information from the POLITICIAN DATA section below. Never invent facts.
- If someone asks about a politician not in the database, say:
  "Wala pa akong data para sa kandidatong iyon. / I don't have data on that candidate yet."
- Be neutral. Never endorse or criticize any candidate.
- Keep answers short and easy to read — many users are on mobile.
- Reply in the same language the user writes in (Filipino or English).
- Never discuss anything unrelated to Philippine politics or the candidates in the database.
- You may tell users which election cycle and category a candidate belongs to.

POLITICIAN DATA:
{POLITICIAN_DATA}
"""

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Nunito:wght@400;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #f5f5f0;
    font-family: 'Nunito', sans-serif;
    color: #111;
}
[data-testid="stHeader"], #MainMenu, footer { display: none; }
[data-testid="stSidebar"] { display: none; }
[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="block-container"] { padding: 0 !important; max-width: 100% !important; }

.nav {
    background: #fff;
    border-bottom: 2px solid #eee;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 99;
}
.wordmark { font-family: 'Archivo Black', sans-serif; font-size: 1.6rem; letter-spacing: -1px; line-height: 1; }
.n  { color: #e63946; }
.o1 { color: #111; }
.b1 { color: #1d3557; }
.o2 { color: #111; }
.b2 { color: #f4a261; }
.o3 { color: #111; }

.stButton > button {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 100px !important;
    border: 2px solid transparent !important;
    padding: 10px 22px !important;
    font-size: 0.9rem !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
    background: #f0f0eb !important;
    color: #555 !important;
    width: 100% !important;
}
.stButton > button:hover { background: #e8e8e2 !important; color: #111 !important; }

.hero {
    background: #fff;
    padding: 52px 24px 44px;
    text-align: center;
    border-bottom: 2px solid #eee;
}
.hero-logo {
    font-family: 'Archivo Black', sans-serif;
    font-size: clamp(3.8rem, 15vw, 6.5rem);
    letter-spacing: -3px;
    line-height: 1;
    margin-bottom: 12px;
}
.hero-tag {
    display: inline-block;
    background: #fff3e0;
    color: #e07b2a;
    font-weight: 700;
    font-size: 0.72rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 12px;
    border-radius: 100px;
    margin-bottom: 18px;
    border: 1.5px solid #f4a261;
}
.hero-sub {
    font-size: clamp(1rem, 3.5vw, 1.15rem);
    color: #444;
    max-width: 400px;
    margin: 0 auto 30px;
    line-height: 1.65;
    font-weight: 600;
}
.cta-wrap .stButton > button {
    background: #e63946 !important;
    color: #fff !important;
    font-size: 1.05rem !important;
    padding: 14px 32px !important;
    box-shadow: 0 4px 16px rgba(230,57,70,0.25) !important;
}
.cta-wrap .stButton > button:hover { background: #c1121f !important; }

.page-wrap { max-width: 600px; margin: 0 auto; padding: 24px 16px 60px; }
.card { background: #fff; border-radius: 18px; border: 2px solid #eee; padding: 22px 20px; margin-bottom: 14px; }
.card h2 { font-family: 'Archivo Black', sans-serif; font-size: 1.1rem; margin: 0 0 8px; color: #111; }
.card p, .card li { color: #555; font-size: 0.9rem; line-height: 1.7; }
.card ul { padding-left: 18px; margin: 0; }
.card li { margin-bottom: 3px; }
.chip { display: inline-block; background: #fff0f0; color: #e63946; border-radius: 6px; padding: 1px 7px; font-size: 0.82rem; font-weight: 700; }

.chat-area { max-width: 600px; margin: 0 auto; padding: 20px 16px 8px; }
.bubble-row-user { display: flex; justify-content: flex-end; margin-bottom: 10px; }
.bubble-row-bot  { display: flex; justify-content: flex-start; margin-bottom: 10px; }
.bubble-user {
    background: #e63946; color: #fff;
    padding: 11px 16px;
    border-radius: 20px 20px 4px 20px;
    max-width: 78%; font-size: 0.92rem; font-weight: 600; line-height: 1.5;
}
.bubble-bot {
    background: #fff; border: 2px solid #eee; color: #111;
    padding: 12px 16px;
    border-radius: 20px 20px 20px 4px;
    max-width: 84%; font-size: 0.92rem; line-height: 1.65;
}
.bot-name { font-size: 0.67rem; font-weight: 700; color: #bbb; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 4px; margin-left: 2px; }

.input-area { max-width: 600px; margin: 0 auto; padding: 0 16px 20px; }
[data-testid="stTextInput"] input {
    background: #fff !important; border: 2px solid #ddd !important;
    border-radius: 100px !important; color: #111 !important;
    padding: 13px 22px !important;
    font-family: 'Nunito', sans-serif !important; font-size: 0.95rem !important; font-weight: 600 !important;
}
[data-testid="stTextInput"] input:focus { border-color: #e63946 !important; box-shadow: 0 0 0 3px rgba(230,57,70,0.1) !important; }
[data-testid="stTextInput"] label { display: none !important; }

.send-col .stButton > button { background: #e63946 !important; color: #fff !important; padding: 13px 18px !important; font-size: 1.1rem !important; }
.send-col .stButton > button:hover { background: #c1121f !important; }
.clear-wrap .stButton > button { background: transparent !important; color: #ccc !important; font-size: 0.8rem !important; padding: 6px 14px !important; border: 1.5px solid #e8e8e2 !important; width: auto !important; }

.footer { text-align: center; color: #ccc; font-size: 0.75rem; padding: 20px 0 48px; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "messages" not in st.session_state:
    st.session_state.messages = []

WORDMARK = '<span class="wordmark"><span class="n">N</span><span class="o1">O</span><span class="b1">B</span><span class="o2">O</span><span class="b2">B</span><span class="o3">O</span></span>'

# ── NAV ───────────────────────────────────────────────────────────────────────
st.markdown(f'<div class="nav">{WORDMARK}<div></div></div>', unsafe_allow_html=True)
_, nc1, nc2, nc3 = st.columns([3.5, 1, 1, 1.3])
with nc1:
    if st.button("Home"):
        st.session_state.page = "home"; st.rerun()
with nc2:
    if st.button("About"):
        st.session_state.page = "about"; st.rerun()
with nc3:
    if st.button("💬 Chatbot"):
        st.session_state.page = "chat"; st.rerun()
st.markdown("<hr style='margin:0;border:none;border-top:2px solid #eee;'>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero">
        <div class="hero-tag">🗳️ Philippine Elections</div>
        <div class="hero-logo">
            <span class="n">N</span><span class="o1">O</span><span class="b1">B</span><span class="o2">O</span><span class="b2">B</span><span class="o3">O</span>
        </div>
        <div class="hero-sub">
            <strong>Know Before You Vote.</strong><br>
            Ask about any candidate — their record,<br>
            contributions, and public info.
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, cta, _ = st.columns([1, 2, 1])
    with cta:
        st.markdown('<div class="cta-wrap">', unsafe_allow_html=True)
        if st.button("💬 Ask the Chatbot"):
            st.session_state.page = "chat"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <h2>What can I ask?</h2>
        <ul>
            <li>Sino si <span class="chip">kandidato</span>?</li>
            <li>Anong partido ang kinabibilangan niya?</li>
            <li>What bills has this senator authored?</li>
            <li>Who funded their campaign?</li>
            <li>What is their voting record?</li>
        </ul>
    </div>
    <div class="card">
        <h2>🔒 No login needed</h2>
        <p>Just open and ask. No account, no tracking, no ads.
        Built for every Filipino voter — kahit saan, kahit sino.</p>
    </div>
    <div class="footer">
        NOBOBO · Know Before You Vote<br>
        Free civic tool · Not affiliated with any political party
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ABOUT
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "about":
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <h2>About NOBOBO</h2>
        <p><strong>NOBOBO</strong> (Know Before You Vote) is a free, non-partisan
        civic tool that helps Filipino voters quickly find public information
        about candidates and elected officials — straight from their records.</p>
        <p style="margin-top:10px;">No spin. No ads. Just facts.</p>
    </div>
    <div class="card">
        <h2>📂 Data Sources</h2>
        <ul>
            <li>COMELEC official filings</li>
            <li>Senate &amp; House of Representatives records</li>
            <li>SALN (Statement of Assets, Liabilities &amp; Net Worth)</li>
            <li>Official government websites</li>
            <li>Verified public news reports</li>
        </ul>
    </div>
    <div class="card">
        <h2>⚠️ Disclaimer</h2>
        <p>NOBOBO is an independent civic project. It is <strong>not affiliated</strong>
        with any political party, candidate, or government agency.</p>
        <p style="margin-top:8px;">The AI may occasionally make mistakes.
        Always verify critical information through official sources like
        <strong>comelec.gov.ph</strong>.</p>
    </div>
    <div class="card">
        <h2>💻 Open Source</h2>
        <p>This project is open source under the <strong>MIT License</strong>.
        Anyone can view, contribute to, or build on the code.</p>
    </div>
    <div class="footer">NOBOBO · Know Before You Vote</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CHAT
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "chat":
    st.markdown("""
    <div style="text-align:center; padding:28px 16px 12px; background:#fff; border-bottom:2px solid #eee;">
        <div style="font-family:'Archivo Black',sans-serif; font-size:1.5rem; color:#111; margin-bottom:4px;">
            💬 Ask NOBOBO
        </div>
        <div style="color:#aaa; font-size:0.85rem; font-family:'Nunito',sans-serif;">
            Type a candidate's name or ask anything about them.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="chat-area">', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown("""
        <div class="bubble-row-bot">
            <div>
                <div class="bot-name">NOBOBO</div>
                <div class="bubble-bot">
                    Kumusta! 👋 I'm NOBOBO.<br>
                    Ask me about any Philippine candidate — their party,
                    bills filed, campaign donors, or public record.<br><br>
                    <em style="color:#bbb; font-size:0.83rem;">Try: "Who is [candidate name]?"</em>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="bubble-row-user"><div class="bubble-user">{msg["content"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bubble-row-bot"><div><div class="bot-name">NOBOBO</div><div class="bubble-bot">{msg["content"]}</div></div></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Input
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    inp_col, send_col = st.columns([5, 1])
    with inp_col:
        user_input = st.text_input("msg", placeholder="Sino ang kandidato mo?", label_visibility="collapsed")
    with send_col:
        st.markdown('<div class="send-col">', unsafe_allow_html=True)
        send = st.button("→")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if send and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *[{"role": m["role"], "content": m["content"]}
                      for m in st.session_state.messages]
                ],
                max_tokens=512,
            )
            reply = response.choices[0].message.content
        except Exception:
            reply = "⚠️ Hindi ako makakonekta ngayon. Please try again in a moment."

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.session_state.messages:
        st.markdown('<div class="input-area"><div class="clear-wrap">', unsafe_allow_html=True)
        if st.button("🗑️ Clear chat"):
            st.session_state.messages = []
            st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="footer">AI may make mistakes. Always verify through official sources.</div>', unsafe_allow_html=True)
