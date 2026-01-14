import streamlit as st
import agent

st.set_page_config(
    page_title="AutoStream AI Agent",
    page_icon="🎬",
    layout="centered"
)

st.title("AutoStream AI Assistant")
st.caption("Social-to-Lead Agentic Workflow")

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Chat input ---
user_input = st.chat_input("Type your message...")

if user_input:
    # 1️⃣ Store user message FIRST
    st.session_state.messages.append(("user", user_input))

    # 2️⃣ Get agent response
    response = agent.process_user_input(user_input)

    # 3️⃣ Store assistant message
    st.session_state.messages.append(("assistant", response))

    # 4️⃣ Force rerun so messages render immediately
    st.rerun()

# --- Render chat history AFTER state updates ---
for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(msg)
