import streamlit as st
import openai

# --- Configuration ---
st.set_page_config(page_title="AgriNova Assistant", layout="centered")
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Store securely in Streamlit secrets

# --- Styling ---
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; }
        .stTextInput > div > div > input { font-size: 16px; }
        .stChatMessage { margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("### 🌱 AgriNova Assistant")
st.markdown("Ask me anything about crops, irrigation, or fertilizers!")

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are AgriNova, a helpful agricultural assistant for farmers in India."}
    ]

# --- Chat Display ---
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User Input ---
user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.markdown(reply)
