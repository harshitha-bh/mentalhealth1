import streamlit as st
import openai
import json
import os

# === OpenAI API Setup ===
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Set this in Streamlit Cloud Secrets

# === File to Store Users ===
USER_FILE = "users.json"
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

# === Load & Save Users ===
def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# === Chatbot Logic ===
def get_chatbot_reply(history):
    messages = [{"role": "system", "content": (
        "You are Solace AI, a friendly and supportive mental health chatbot. "
        "If the user shares emotional or sensitive content, respond kindly with empathy, encouragement, and optional calming exercises or quotes. "
        "If the user is chatting normally, just reply like a close friend using emojis and casual Tenglish."
    )}]
    for role, msg in history:
        messages.append({"role": "user" if role == "user" else "assistant", "content": msg})
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

# === Session State Defaults ===
defaults = {
    "authenticated": False,
    "username": "",
    "page": "Login",
    "chat_history": [],
    "users": load_users()
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# === Custom UI CSS ===
st.set_page_config("Solace AI", layout="centered")
st.markdown("""
<style>
body { background-color: #f7f3fc; }
h1, h2, h3 { color: #6a1b9a; text-align: center; }
.message {
    padding: 12px 16px; border-radius: 12px; margin: 8px 0;
    font-size: 15px; line-height: 1.5; max-width: 85%;
    word-wrap: break-word; box-shadow: 1px 2px 6px rgba(0,0,0,0.08);
}
.user { background: #fce4ec; color: #880e4f; margin-left: auto; text-align: right; }
.bot { background: #e3f2fd; color: #0d47a1; margin-right: auto; text-align: left; }
</style>
""", unsafe_allow_html=True)

# === Login Page ===
def login_page():
    st.title("🔐 Login to Solace AI")
    with st.form("login_form", clear_on_submit=True):
        uname = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")
        if login_btn:
            users = st.session_state.users
            if uname in users and users[uname] == pwd:
                st.session_state.authenticated = True
                st.session_state.username = uname
                st.success("✅ Logged in successfully!")
                st.session_state.page = "Chat"
            else:
                st.error("❌ Invalid credentials. Please sign up.")

# === Signup Page ===
def signup_page():
    st.title("📝 Sign Up for Solace AI")
    with st.form("signup_form", clear_on_submit=True):
        uname = st.text_input("Choose a Username")
        pwd1 = st.text_input("Password", type="password")
        pwd2 = st.text_input("Confirm Password", type="password")
        signup_btn = st.form_submit_button("Sign Up")
        if signup_btn:
            users = st.session_state.users
            if uname in users:
                st.error("🚫 Username already exists.")
            elif not uname or not pwd1 or not pwd2:
                st.warning("⚠️ Please fill all fields.")
            elif pwd1 != pwd2:
                st.warning("⚠️ Passwords don’t match.")
            else:
                users[uname] = pwd1
                save_users(users)
                st.session_state.users = users
                st.success("🎉 Signed up successfully! Please log in.")
                st.session_state.page = "Login"

# === Chat Interface ===
def chat_interface():
    st.markdown("<h1>🌿 Solace AI</h1>", unsafe_allow_html=True)
    st.markdown("Welcome to your personal mental health companion and chat friend 💬")

    for role, msg in st.session_state.chat_history:
        css = "user" if role == "user" else "bot"
        st.markdown(f"<div class='message {css}'>{msg}</div>", unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message", key="chat_input", label_visibility="collapsed")
        send = st.form_submit_button("Send")
        if send and user_input.strip():
            st.session_state.chat_history.append(("user", user_input))
            with st.spinner("Solace is typing..."):
                reply = get_chatbot_reply(st.session_state.chat_history)
            st.session_state.chat_history.append(("bot", reply))
            st.experimental_rerun()

    st.sidebar.title("🔑 Account")
    st.sidebar.write(f"👤 Logged in as: `{st.session_state.username}`")
    if st.sidebar.button("Logout"):
        for key in ["authenticated", "username", "chat_history"]:
            st.session_state[key] = defaults[key]
        st.session_state.page = "Login"
        st.success("👋 Logged out successfully.")
        st.experimental_rerun()

# === Main App Routing ===
if not st.session_state.authenticated:
    st.sidebar.title("Navigation")
    st.session_state.page = st.sidebar.radio("Choose", ["Login", "Sign Up"])
    login_page() if st.session_state.page == "Login" else signup_page()
else:
    chat_interface()
