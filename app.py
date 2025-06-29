import streamlit as st
import openai
import json
import os

# === Configuration ===
st.set_page_config("Solace AI 💬", layout="centered")
openai.api_key = st.secrets["OPENAI_API_KEY"]
USER_FILE = "users.json"

# === State Init ===
if "auth" not in st.session_state:
    st.session_state.auth = False
if "page" not in st.session_state:
    st.session_state.page = "Login"
if "chat" not in st.session_state:
    st.session_state.chat = []
if "username" not in st.session_state:
    st.session_state.username = ""

# === Load / Save users ===
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

# === Get reply from OpenAI ===
def get_reply(user_input):
    messages = [
        {"role": "system", "content": "You're Solace AI, a supportive and friendly chatbot who responds casually like a close friend. If user sounds sad, offer motivation. Otherwise, chat normally using emojis."},
        {"role": "user", "content": user_input}
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# === Signup Page ===
def signup_page():
    st.title("📝 Create an Account")
    new_user = st.text_input("Choose a username", key="signup_user")
    new_pass = st.text_input("Choose a password", type="password", key="signup_pass")
    confirm = st.text_input("Confirm password", type="password", key="signup_confirm")
    if st.button("Sign Up"):
        users = load_users()
        if not new_user or not new_pass:
            st.warning("All fields required.")
        elif new_user in users:
            st.error("Username already exists.")
        elif new_pass != confirm:
            st.error("Passwords don't match.")
        else:
            users[new_user] = new_pass
            save_users(users)
            st.success("✅ Signup successful! Please log in.")
            st.session_state.page = "Login"

# === Login Page ===
def login_page():
    st.title("🔐 Login")
    user = st.text_input("Username", key="login_user")
    pwd = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        users = load_users()
        if user in users and users[user] == pwd:
            st.session_state.auth = True
            st.session_state.username = user
            st.session_state.chat = []
            st.success("✅ Login successful!")
            st.session_state.page = "Chat"
        else:
            st.error("❌ Incorrect login. Try again or sign up.")

# === Chat Page ===
def chat_page():
    st.markdown(f"<h2 style='color:#6a1b9a;'>Welcome, {st.session_state.username} 🌸</h2>", unsafe_allow_html=True)
    st.divider()

    for sender, msg in st.session_state.chat:
        align = "right" if sender == "user" else "left"
        bg = "#f8bbd0" if sender == "user" else "#bbdefb"
        color = "#880e4f" if sender == "user" else "#0d47a1"
        st.markdown(
            f"<div style='background:{bg}; color:{color}; padding:10px; margin:10px 0; border-radius:10px; max-width:75%; text-align:{align};'>{msg}</div>",
            unsafe_allow_html=True,
        )

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message...")
        send = st.form_submit_button("Send")
        if send and user_input:
            st.session_state.chat.append(("user", user_input))
            reply = get_reply(user_input)
            st.session_state.chat.append(("bot", reply))

    if st.sidebar.button("Logout"):
        for key in ["auth", "username", "chat", "page"]:
            st.session_state.pop(key, None)
        st.rerun()

# === Page Control ===
if not st.session_state.auth:
    st.sidebar.title("🔄 Navigation")
    st.session_state.page = st.sidebar.radio("Choose", ["Login", "Sign Up"])
    if st.session_state.page == "Login":
        login_page()
    else:
        signup_page()
else:
    chat_page()
