import streamlit as st
import openai
import json
import os

st.set_page_config(page_title="Solace AI - Mental Health Chatbot", layout="centered")

# Load OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# JSON file to store users
USER_FILE = "users.json"

# Session initialization
if "auth" not in st.session_state:
    st.session_state.auth = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat" not in st.session_state:
    st.session_state.chat = []

# Functions for user handling
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# OpenAI reply generator
def get_reply(message):
    messages = [
        {"role": "system", "content": (
            "You are Solace AI, a supportive mental health chatbot. "
            "When user shares feelings, respond with empathy, a motivational quote, and a calming exercise. "
            "When chat is casual, act like a friendly buddy and use emojis."
        )},
        {"role": "user", "content": message}
    ]
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

# Signup page
def signup_page():
    st.title("📝 Create Your Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        users = load_users()
        if new_user in users:
            st.error("🚫 Username already exists! Try logging in.")
        elif not new_user or not new_pass or not confirm_pass:
            st.warning("⚠️ Please fill all fields.")
        elif new_pass != confirm_pass:
            st.error("🔁 Passwords do not match.")
        else:
            users[new_user] = new_pass
            save_users(users)
            st.success("✅ Signup successful! Please login now.")

# Login page
def login_page():
    st.title("🔐 Login to Solace AI")
    user = st.text_input("Username", key="login_user")
    pwd = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        users = load_users()
        if user in users and users[user] == pwd:
            st.session_state.auth = True
            st.session_state.username = user
            st.session_state.chat = []
            st.success(f"✅ Welcome back, {user}! You’re now logged in.")
        else:
            st.error("❌ Invalid credentials. Please sign up if you’re new.")

# Chat interface
def chat_page():
    st.markdown("<h2 style='color:#6a1b9a;'>💬 Solace AI - Mental Health Support Chatbot</h2>", unsafe_allow_html=True)
    st.caption("You can share anything with me — I'm here to support you 💜")

    for sender, msg in st.session_state.chat:
        align = "right" if sender == "user" else "left"
        color = "#fce4ec" if sender == "user" else "#e8f5e9"
        st.markdown(
            f"<div style='text-align:{align}; background-color:{color}; padding:10px; "
            f"border-radius:10px; margin:5px; max-width:70%; color:#000;'>{msg}</div>",
            unsafe_allow_html=True
        )

    user_input = st.text_input("Type your message here...", key="input_text", placeholder="How are you feeling today?")
    send = st.button("Send 💬")

    if send and user_input.strip():
        msg = user_input.strip()
        st.session_state.chat.append(("user", msg))
        reply = get_reply(msg)
        st.session_state.chat.append(("bot", reply))
        st.experimental_rerun()  # Refresh to clear input and show reply

    if st.button("Logout 🚪"):
        st.session_state.auth = False
        st.session_state.username = ""
        st.session_state.chat = []
        st.success("You’ve been logged out. See you soon!")

# Main app logic
def main():
    st.sidebar.title("🌼 Solace AI")
    st.sidebar.caption("Your personal mental health support companion.")
    if not st.session_state.auth:
        page = st.sidebar.radio("Navigation", ["Login", "Sign Up"])
        if page == "Login":
            login_page()
        else:
            signup_page()
    else:
        chat_page()

main()
