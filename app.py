import streamlit as st
import json
import os
import uuid
import openai

st.set_page_config(page_title="Solace AI - Mental Health Support", layout="centered")

# Load or create users database
USER_DB = "users.json"
if not os.path.exists(USER_DB):
    with open(USER_DB, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_DB, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

# Style (injected CSS)
st.markdown("""
    <style>
        body { background-color: #f7f6fb; }
        .stTextInput > div > div > input {
            color: #333;
            font-weight: 500;
            background-color: #ffffff;
            border-radius: 10px;
        }
        .stButton>button {
            background-color: #6a8caf;
            color: white;
            border-radius: 8px;
            padding: 8px 16px;
        }
        .user-message { background-color: #e0f7fa; padding: 10px; border-radius: 8px; margin-bottom: 8px; }
        .bot-message { background-color: #fce4ec; padding: 10px; border-radius: 8px; margin-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

# OpenAI API Key (must be set in Streamlit Secrets for deployment)
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_reply(message_history):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_history,
        temperature=0.7,
        max_tokens=300
    )
    return response.choices[0].message["content"].strip()

# Session initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "login"

# Auth Pages
def signup_page():
    st.title("🧾 Sign Up")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Create Account"):
        users = load_users()
        if email in users:
            st.warning("🚫 Email already exists. Please log in.")
        else:
            users[email] = {"password": password}
            save_users(users)
            st.success("✅ Signup successful! Please log in.")
            st.session_state.mode = "login"

def login_page():
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        users = load_users()
        if email in users and users[email]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.username = email
            st.session_state.mode = "chat"
            st.success("✅ Logged in successfully!")
        else:
            st.warning("❌ Incorrect credentials or not signed up. Please try again.")

# Chat Page
def chat_page():
    st.title("🧠 Solace AI - Mental Health Support Chatbot")
    st.markdown("Welcome to your safe space. Share your thoughts, or just chat casually 😊")

    # Display past messages
    for role, msg in st.session_state.messages:
        style = "user-message" if role == "user" else "bot-message"
        st.markdown(f"<div class='{style}'>{'🧍‍♀️' if role=='user' else '🤖'} {msg}</div>", unsafe_allow_html=True)

    # Chat input
    user_input = st.text_input("Type your message", key="chat_input")

    if st.button("Send"):
        if user_input.strip():
            st.session_state.messages.append(("user", user_input))
            mood_keywords = ["sad", "depressed", "tired", "angry", "lonely", "worried", "upset"]
            emotional = any(word in user_input.lower() for word in mood_keywords)

            prompt = (
                "You are a friendly and emotionally intelligent chatbot named Solace AI. "
                "When the user shares emotional distress, you respond supportively with empathy, quotes, and exercises. "
                "If they chat normally, respond like a fun and casual friend using emojis."
            )

            message_history = [{"role": "system", "content": prompt}]
            for role, msg in st.session_state.messages[-5:]:
                message_history.append({"role": role, "content": msg})

            reply = generate_reply(message_history)
            st.session_state.messages.append(("assistant", reply))
            st.session_state.chat_input = ""  # Clear input

# App Flow
def main():
    if not st.session_state.authenticated:
        if st.session_state.mode == "signup":
            signup_page()
        else:
            login_page()
            st.markdown("👉 Don't have an account? [Sign up here](#)", unsafe_allow_html=True)
            if st.button("Go to Signup"):
                st.session_state.mode = "signup"
    else:
        chat_page()

main()
