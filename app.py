import streamlit as st
import openai
import json
import os

# Setup
st.set_page_config("Solace AI 💬", layout="centered")
openai.api_key = st.secrets["OPENAI_API_KEY"]
USER_FILE = "users.json"

# Initialize session state
if "auth" not in st.session_state:
    st.session_state.auth = False
if "page" not in st.session_state:
    st.session_state.page = "Login"
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat" not in st.session_state:
    st.session_state.chat = []

# Load and Save user data
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

# OpenAI reply function
def get_reply(user_input):
    messages = [
        {"role": "system", "content": "You are Solace AI, a supportive mental health chatbot."},
        {"role": "user", "content": user_input}
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Signup Page
def signup_page():
    st.title("📝 Sign Up")
    with st.form("signup_form"):
        new_user = st.text_input("Choose a username")
        new_pass = st.text_input("Choose a password", type="password")
        confirm_pass = st.text_input("Confirm password", type="password")
        submit = st.form_submit_button("Create Account")

        if submit:
            users = load_users()
            if new_user in users:
                st.error("Username already exists. Try logging in.")
            elif new_pass != confirm_pass:
                st.error("Passwords do not match.")
            elif not new_user or not new_pass:
                st.warning("Please fill all fields.")
            else:
                users[new_user] = new_pass
                save_users(users)
                st.success("✅ Signed up successfully! Please log in.")
                st.session_state.page = "Login"

# Login Page
def login_page():
    st.title("🔐 Login")
    with st.form("login_form"):
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")

        if login_btn:
            users = load_users()
            if user in users and users[user] == pwd:
                st.session_state.auth = True
                st.session_state.username = user
                st.session_state.page = "Chat"
                st.success("✅ Logged in successfully!")
            else:
                st.error("❌ Invalid username or password.")

# Chat Page
def chat_page():
    st.markdown(f"<h1 style='text-align:center;color:#6a1b9a;'>Solace AI 💬</h1>", unsafe_allow_html=True)
    st.markdown(f"👋 Welcome, `{st.session_state.username}`")
    st.divider()

    for sender, msg in st.session_state.chat:
        role = "user" if sender == "user" else "bot"
        bg = "#fce4ec" if role == "user" else "#e3f2fd"
        color = "#880e4f" if role == "user" else "#0d47a1"
        align = "right" if role == "user" else "left"
        st.markdown(
            f"<div style='background:{bg}; color:{color}; padding:10px; border-radius:10px; margin:10px 0; max-width:80%; text-align:{align};'>{msg}</div>",
            unsafe_allow_html=True,
        )

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("You:", key="chat_input")
        send = st.form_submit_button("Send")
        if send and user_input:
            st.session_state.chat.append(("user", user_input))
            reply = get_reply(user_input)
            st.session_state.chat.append(("bot", reply))

    st.sidebar.markdown("🔚 [Logout](#)", unsafe_allow_html=True)
    if st.sidebar.button("Logout"):
        for k in ["auth", "username", "chat", "page"]:
            st.session_state[k] = False if k == "auth" else "" if k == "username" else []
        st.rerun()

# Routing logic
if not st.session_state.auth:
    st.sidebar.title("Navigation")
    st.session_state.page = st.sidebar.radio("Choose", ["Login", "Sign Up"])
    if st.session_state.page == "Login":
        login_page()
    else:
        signup_page()
else:
    chat_page()
