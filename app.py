import streamlit as st
from rag import ask_question

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Company Policy AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: #FFFFFF;
}

[data-testid="stSidebar"] {
    background-color: #161B22;
    border-right: 1px solid #30363D;
}

.main-title {
    font-size: 36px;
    font-weight: 800;
    color: #FFFFFF;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #9CA3AF;
    font-size: 16px;
    margin-bottom: 30px;
}

.chat-user {
    background-color: #263449;
    padding: 15px 20px;
    border-radius: 15px 15px 3px 15px;
    margin: 12px 0;
    margin-left: 15%;
}

.chat-assistant {
    background-color: #1C2431;
    padding: 18px 20px;
    border-radius: 15px 15px 15px 3px;
    margin: 12px 0;
    margin-right: 10%;
    border: 1px solid #303D50;
}

.chat-label {
    font-size: 13px;
    font-weight: bold;
    color: #60A5FA;
    margin-bottom: 8px;
}

.status-card {
    background-color: #1C2431;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #30363D;
    text-align: center;
}

div.stButton > button {
    border-radius: 10px;
    border: 1px solid #374151;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("## 🤖 Policy AI")

    st.caption("Intelligent Company Knowledge Assistant")

    st.divider()

    st.markdown("### ⚙️ Configuration")

    st.success("OpenAI Connected")
    st.success("Pinecone RAG Enabled")

    st.divider()

    st.markdown("### 💡 Suggested Questions")

    suggestions = [
        "How many paid leaves are available?",
        "What is the leave policy?",
        "What are the company working hours?",
        "What is the work from home policy?"
    ]

    for question in suggestions:
        if st.button(question, use_container_width=True):
            st.session_state.pending_question = question

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pop("pending_question", None)
        st.rerun()

    st.markdown("---")
    st.caption("Powered by OpenAI + Pinecone")


# ---------------- MAIN HEADER ----------------

st.markdown(
    '<div class="main-title">🤖 Company Policy Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask questions about company policies and get intelligent answers instantly.</div>',
    unsafe_allow_html=True
)


# ---------------- WELCOME SECTION ----------------

if not st.session_state.messages:

    st.markdown("### 👋 Welcome!")

    st.markdown(
        """
        <div class="status-card">
            <h3>How can I help you today?</h3>
            <p style="color:#9CA3AF;">
            I can answer questions about company policies using
            Retrieval Augmented Generation (RAG).
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.markdown("#### Try asking something")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📅 Leave Policy", use_container_width=True):
            st.session_state.pending_question = "Explain the company leave policy."

        if st.button("🏢 Office Timings", use_container_width=True):
            st.session_state.pending_question = "What are the company office timings?"

    with col2:
        if st.button("🏠 Work From Home", use_container_width=True):
            st.session_state.pending_question = "Explain the work from home policy."

        if st.button("💰 Salary Policy", use_container_width=True):
            st.session_state.pending_question = "Explain the salary policy."


# ---------------- DISPLAY CHAT HISTORY ----------------

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="chat-user">
                <div class="chat-label">👤 YOU</div>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="chat-assistant">
                <div class="chat-label">🤖 AI ASSISTANT</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(message["content"])


# ---------------- CHAT INPUT ----------------

question = st.chat_input("Ask anything about company policies...")

pending_question = st.session_state.pop(
    "pending_question", None
)

user_question = question or pending_question


# ---------------- GENERATE RESPONSE ----------------

if user_question:

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.spinner("🔍 Searching company documents and generating answer..."):

        try:
            answer = ask_question(user_question)

        except Exception as e:
            answer = f"Something went wrong: {str(e)}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()
