import streamlit as st
import openai
import os
import json

# --- OpenAI API Key ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Users File ---
USER_FILE = "users.json"
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

# --- Load and Save User Data ---
def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# --- Chatbot Response Logic ---
def get_chatbot_reply(user_input):
    messages = [
        {"role": "system", "content": (
            "You are Solace AI, a kind and casual mental health companion. "
            "If user shares emotional pain, respond warmly with quotes and calming tips. "
            "If user chats normally, reply casually like a close friend using emojis."
        )},
        {"role": "user", "content": user_input}
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

# --- Session State Initialization ---
for k, v in {
    "auth": False,
    "username": "",
    "page": "Login",
    "users": load_users(),
    "chat": [],
    "show_chatbot": False
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- Page Setup and Custom CSS ---
st.set_page_config("Solace AI", layout="centered")
st.markdown("""
<style>
.title { color: #6a1b9a; text-align: center; font-weight: bold; font-size: 2.4em; }
.subtitle { text-align: center; font-style: italic; color: #555; }
.message {
    padding: 12px 16px; border-radius: 12px; margin: 8px 0;
    font-size: 15px; line-height: 1.5; max-width: 85%;
    word-wrap: break-word; box-shadow: 1px 2px 6px rgba(0,0,0,0.08);
}
.user { background: #fce4ec; color: #880e4f; margin-left: auto; text-align: right; }
.bot { background: #e3f2fd; color: #0d47a1; margin-right: auto; text-align: left; }
</style>
""", unsafe_allow_html=True)

# --- Login Page ---
def login_page():
    st.title("🔐 Login to Solace AI")
    with st.form("login_form", clear_on_submit=True):
        uname = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        login = st.form_submit_button("Login")
        if login:
            users = load_users()
            if uname in users and users[uname] == pwd:
                st.session_state.auth = True
                st.session_state.username = uname
                st.success(f"✅ Logged in successfully! Welcome, {uname} 🎉")
                st.session_state.page = "Dashboard"
            else:
                st.error("❌ Invalid credentials. Please sign up if you’re new.")

# --- Signup Page ---
def signup_page():
    st.title("📝 Sign Up for Solace AI")
    with st.form("signup_form", clear_on_submit=True):
        uname = st.text_input("Choose a Username")
        pwd = st.text_input("Choose a Password", type="password")
        signup = st.form_submit_button("Sign Up")
        if signup:
            if not uname or not pwd:
                st.warning("⚠️ Please fill all fields.")
            else:
                users = load_users()
                if uname in users:
                    st.error("⚠️ Username already exists. Try a different one.")
                else:
                    users[uname] = pwd
                    save_users(users)
                    st.success("🎊 Signed up successfully! You can now log in.")
                    st.session_state.page = "Login"

# --- Dashboard After Login ---
def dashboard():
    st.title(f"👋 Welcome, {st.session_state.username}")
    st.markdown("You're now logged in to **Solace AI**, your friendly mental health support companion 💬")
    if st.button("🧠 Start Chatbot"):
        st.session_state.show_chatbot = True
        st.rerun()

# --- Chat Page ---
def chat_page():
    st.markdown("<h1 class='title'>🌿 Solace AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>I’m your mental health supporter and a good friend 💗</p>", unsafe_allow_html=True)

    for role, msg in st.session_state.chat:
        css = "user" if role == "user" else "bot"
        st.markdown(f"<div class='message {css}'>{msg}</div>", unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message", label_visibility="collapsed")
        send = st.form_submit_button("Send")
        if send and user_input.strip():
            st.session_state.chat.append(("user", user_input))
            with st.spinner("Solace is typing..."):
                reply = get_chatbot_reply(user_input)
            st.session_state.chat.append(("bot", reply))
            st.rerun()

    st.sidebar.title("🔑 Account")
    st.sidebar.write(f"Logged in as: `{st.session_state.username}`")
    if st.sidebar.button("Logout"):
        for key in ["auth", "username", "page", "show_chatbot", "chat"]:
            st.session_state[key] = False if isinstance(st.session_state[key], bool) else ""
        st.session_state.chat = []
        st.rerun()

# --- Page Routing ---
if not st.session_state.auth:
    st.sidebar.title("🔐 Access")
    st.session_state.page = st.sidebar.radio("Go to", ["Login", "Sign Up"])
    if st.session_state.page == "Login":
        login_page()
    else:
        signup_page()
elif st.session_state.show_chatbot:
    chat_page()
else:
    dashboard()
