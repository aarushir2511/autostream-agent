import streamlit as st
import agent

st.set_page_config(
    page_title="AutoStream AI Agent",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 AutoStream AI Assistant")
st.caption("Social-to-Lead Agentic Workflow")

if "messages" not in st.session_state:
    st.session_state.messages = []

for role, msg in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(msg)

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append(("user", user_input))

    response = agent.process_user_input(user_input)

    st.session_state.messages.append(("assistant", response))

    with st.chat_message("assistant"):
        st.markdown(response)
