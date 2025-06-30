import streamlit as st
import json
import os
import openai

# Set your OpenAI API key here or in Streamlit secrets
openai.api_key = st.secrets.get("OPENAI_API_KEY", "sk-...")

# Set page configuration
st.set_page_config(page_title="Solace AI – Mental Health Chatbot", page_icon="🧠", layout="centered")

# === SESSION STATE SETUP ===
defaults = {
    "authenticated": False,
    "mode": "login",
    "username": "",
    "messages": [],
    "chat_input": ""
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# === USER DATA FILE ===
USER_FILE = "users.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

# === Load users ===
def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

# === Save users ===
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# === Authentication UI ===
def login_page():
    st.markdown("## 🔐 Login to Solace AI")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()
        if username in users and users[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("✅ Logged in successfully!")
        else:
            st.error("❌ Incorrect credentials. Please sign up if you're new.")

    st.markdown("Don't have an account? [Click to Sign Up](#)", unsafe_allow_html=True)
    if st.button("Go to Sign Up"):
        st.session_state.mode = "signup"

def signup_page():
    st.markdown("## 📝 Create an Account")
    new_user = st.text_input("Choose a username")
    new_pass = st.text_input("Choose a password", type="password")

    if st.button("Sign Up"):
        users = load_users()
        if new_user in users:
            st.warning("⚠️ Username already exists.")
        else:
            users[new_user] = new_pass
            save_users(users)
            st.success("✅ Signed up successfully! Please log in.")
            st.session_state.mode = "login"

    st.markdown("Already have an account? [Click to Login](#)", unsafe_allow_html=True)
    if st.button("Back to Login"):
        st.session_state.mode = "login"

# === Chatbot Response Function ===
def get_response(user_msg):
    system_prompt = (
        "You are Solace, a friendly and empathetic mental health companion. "
        "If the user shares emotions or stress, respond with warmth, empathy, and include a calming quote or breathing exercise. "
        "If the user chats normally, respond casually like a friend with emojis. Keep it short and natural."
    )

    messages = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.messages:
        messages.append(msg)

    messages.append({"role": "user", "content": user_msg})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    bot_reply = response['choices'][0]['message']['content']
    return bot_reply.strip()

# === Chat Interface ===
def chat_page():
    st.markdown("## 💬 Solace AI – Your Mental Health Chat Companion")
    st.write("Talk to me like a friend. I’m here to listen and support you. 🌈")

    # Show message history
    for msg in st.session_state.messages:
        sender = "🤖" if msg["role"] == "assistant" else "🧍‍♀️"
        with st.chat_message(sender):
            st.markdown(msg["content"])

    # User input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Show user message
        st.chat_message("🧍‍♀️").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Typing feedback
        with st.chat_message("🤖"):
            with st.spinner("Solace is typing..."):
                reply = get_response(user_input)
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

# === Main Controller ===
def main():
    if not st.session_state.authenticated:
        if st.session_state.mode == "login":
            login_page()
        elif st.session_state.mode == "signup":
            signup_page()
    else:
        chat_page()

main()
