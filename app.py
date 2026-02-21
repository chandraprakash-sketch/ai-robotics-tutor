# ================== MV Raman High School ==================
# 🤖 ATL – Atal Tinkering Lab | AI STEM Tutor

import json
import streamlit as st
from transformers import pipeline
import streamlit.components.v1 as components

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="MV Raman High School – ATL AI Tutor",
    page_icon="🤖",
    layout="wide"
)

# ------------------ Global CSS ------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: #f4f7fb;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #102a43, #243b55);
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: 1px solid #d0d7e2;
    background: #ffffff;
    color: #102a43;
    font-weight: 600;
    padding: 6px 10px;
    font-size: 13px;
    margin-bottom: 6px;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: #eaf1fb;
    border-color: #1d4ed8;
    color: #1d4ed8;
    transform: translateY(-2px);
}

/* Clear Chat Button */
.clear-chat-btn button {
    width: 100%;
    background: linear-gradient(90deg, #ff6a6a, #ff3d3d) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    border: none !important;
}
.clear-chat-btn button:hover {
    background: linear-gradient(90deg, #ff3d3d, #ff0000) !important;
    transform: scale(1.03);
}

/* Chat bubbles */
div[data-testid="stChatMessage"][aria-label="user"] {
    background: #eaf1fb;
    border-radius: 12px;
    padding: 12px;
}
div[data-testid="stChatMessage"][aria-label="assistant"] {
    background: #ffffff;
    border-radius: 12px;
    padding: 12px;
    border: 1px solid #e1e6ef;
}

/* Code */
pre {
    border-radius: 12px !important;
    background: #f4f7fb !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SINGLE BOX ANIMATED HEADER ------------------
components.html(
"""
<!DOCTYPE html>
<html>
<head>
<style>
body { margin: 0; }

.header-box {
    position: relative;
    width: 100%;
    height: 280px;
    border-radius: 24px;
    overflow: hidden;
    background: linear-gradient(135deg, #eaf3ff, #f7fbff);
    box-shadow: 0 10px 30px rgba(0,0,0,0.12);
}

/* Floating DNA bubbles */
.bubble {
    position: absolute;
    bottom: -120px;
    background: rgba(30, 120, 255, 0.18);
    border-radius: 50%;
    animation: rise 20s infinite ease-in;
    z-index: 1;
}

.bubble:nth-child(1) { width: 120px; height: 120px; left: 5%; animation-duration: 22s; }
.bubble:nth-child(2) { width: 60px; height: 60px; left: 15%; animation-duration: 14s; animation-delay: 2s; }
.bubble:nth-child(3) { width: 90px; height: 90px; left: 30%; animation-duration: 18s; animation-delay: 4s; }
.bubble:nth-child(4) { width: 150px; height: 150px; left: 45%; animation-duration: 26s; animation-delay: 1s; }
.bubble:nth-child(5) { width: 70px; height: 70px; left: 65%; animation-duration: 16s; animation-delay: 3s; }
.bubble:nth-child(6) { width: 110px; height: 110px; left: 80%; animation-duration: 24s; animation-delay: 5s; }

@keyframes rise {
    0% { transform: translateY(0); opacity: 0.35; }
    100% { transform: translateY(-420px); opacity: 0; }
}

/* TEXT OVERLAY */
.header-content {
    position: relative;
    z-index: 2;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-family: Arial, sans-serif;
    color: #0f2a44;
    padding: 20px;
}

.header-content h1 { margin: 0; font-size: 42px; font-weight: 700; }
.header-content h2 { margin: 8px 0; font-size: 28px; color: #1d4ed8; }
.header-content h3 { margin: 6px 0; font-size: 20px; color: #222; }
.header-content p  { margin-top: 6px; font-size: 16px; color: #444; }
</style>
</head>

<body>
<div class="header-box">
    <div class="bubble"></div><div class="bubble"></div><div class="bubble"></div>
    <div class="bubble"></div><div class="bubble"></div><div class="bubble"></div>

    <div class="header-content">
        <h1>🏫 MV Raman High School</h1>
        <h2>🤖 ATL – Atal Tinkering Lab</h2>
        <h3>AI Tutor for Arduino, Robotics & STEM</h3>
        <p>Experience Smart, Interactive & Future-Ready Learning</p>
    </div>
</div>
</body>
</html>
""",
height=300
)

# ------------------ Load AI Model ------------------
@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-base")

qa_bot = load_model()

# ------------------ Load Knowledge Base ------------------
with open("knowledge.json", "r", encoding="utf-8") as f:
    KNOWLEDGE = json.load(f)

# ------------------ Helper Function ------------------
def get_response(user_input: str):
    # Search offline DB first
    for category in KNOWLEDGE:
        for q in KNOWLEDGE[category]:
            if q.lower() in user_input.lower() or user_input.lower() in q.lower():
                return KNOWLEDGE[category][q]

    # AI fallback
    try:
        result = qa_bot("Explain simply: " + user_input, max_length=200)
        return {"answer": result[0]["generated_text"], "code": ""}
    except Exception:
        return {
            "answer": "This question is not in my offline database yet. Please add it to knowledge.json.",
            "code": ""
        }

# ------------------ Sidebar ------------------
st.sidebar.title("🏫 MV Raman High School")
st.sidebar.markdown("""
## 🤖 ATL – Atal Tinkering Lab

**AI Robotics & STEM Innovation Center**
""")

# Clear Chat button (red)
st.sidebar.markdown('<div class="clear-chat-btn">', unsafe_allow_html=True)
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []
st.sidebar.markdown('</div>', unsafe_allow_html=True)

st.sidebar.markdown("---")

selected_topic = st.sidebar.radio(
    "Choose topic:",
    ["All", "basics", "programming", "sensors", "motors", "power", "esp32", "basic_codes"]
)

# ------------------ Chat Memory ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------ Build Question List ------------------
if selected_topic != "All":
    questions = list(KNOWLEDGE.get(selected_topic, {}).keys())
else:
    questions = []
    for cat in KNOWLEDGE:
        questions.extend(KNOWLEDGE[cat].keys())

st.markdown("### 📚 Click a question or ask your own")

# ------------------ BUTTONS (FIXED) ------------------
cols = st.columns(3)
for i, q in enumerate(questions[:90]):
    if cols[i % 3].button(q):
        # User message
        st.session_state.messages.append({"role": "user", "content": q})

        # Get reply
        reply = get_response(q)

        # Assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": reply["answer"],
            "code": reply.get("code", "")
        })

        st.rerun()

# ------------------ Show Chat ------------------
st.markdown("---")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("code"):
            st.code(msg["code"], language="cpp")

# ------------------ Input ------------------
user_input = st.chat_input("Ask your Arduino / Robotics / STEM question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    reply = get_response(user_input)
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply["answer"],
        "code": reply.get("code", "")
    })
    st.rerun()
