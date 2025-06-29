import streamlit as st
import openai
import os
import json

st.set_page_config(page_title="Solace AI - Mental Health Companion", layout="centered")

# Set OpenAI API Key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

USER_FILE = "users.json"

# Load & Save users
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# Get OpenAI reply
def get_chatbot_reply(user_msg):
    system_prompt = (
        "You're Solace AI, a kind and friendly mental health support chatbot. "
        "When users share emotional or personal things, reply with empathy, quotes, and calming techniques. "
        "If they chat casually, just chat back like a close friend using emojis and supportive words."
    )

    messages = [{"role": "system", "content": system_prompt}]
    messages += [{"role": "user", "content": user_msg}]

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

# Sign Up
def signup():
    st.title("📝 Create New Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")
    if st.button("Sign Up"):
        users = load_users()
        if new_user in users:
            st.error("❌ Username already exists!")
        elif new_pass != confirm_pass:
            st.warning("⚠️ Passwords do not match.")
        elif not new_user or not new_pass:
            st.warning("Please fill all the fields.")
        else:
            users[new_user] = new_pass
            save_users(users)
            st.success("✅ Signup successful! Now you can log in.")

# Login
def login():
    st.title("🔐 Login to Solace AI")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        users = load_users()
        if username in users and users[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success(f"✅ Welcome back, {username}!")
        else:
            st.error("❌ Invalid credentials. Please sign up if you're new.")

# Chat Page
def chat_interface():
    st.markdown(f"<h3 style='color:#6a1b9a;'>💬 Welcome, {st.session_state.username}</h3>", unsafe_allow_html=True)
    st.caption("You're now chatting with Solace AI. Feel free to share anything on your mind 💙")

    # Display chat history
    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"<div style='text-align:right; background-color:#fce4ec; padding:10px; border-radius:10px; margin:5px;'>{msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left; background-color:#e8f5e9; padding:10px; border-radius:10px; margin:5px;'>{msg}</div>", unsafe_allow_html=True)

    # Chat input box
    user_input = st.text_input("Type your message here...", key="user_input", placeholder="Talk to Solace AI 💬")

    if st.button("Send"):
        if user_input.strip() == "":
            st.warning("Please type something before sending.")
        else:
            st.session_state.chat_history.append(("user", user_input))
            reply = get_chatbot_reply(user_input)
            st.session_state.chat_history.append(("bot", reply))
            st.session_state["user_input"] = ""  # Clear input box

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.chat_history = []
        st.success("🔒 Logged out successfully.")

# Main
def main():
    st.markdown("<h1 style='text-align:center; color:#4a148c;'>Solace AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px;'>Your personal mental health support companion 🌸</p>", unsafe_allow_html=True)
    st.divider()

    if not st.session_state.authenticated:
        page = st.radio("Choose", ["Login", "Sign Up"], horizontal=True)
        if page == "Login":
            login()
        else:
            signup()
    else:
        chat_interface()

main()
