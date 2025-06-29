import streamlit as st
import openai
import json
import os

# ===== CONFIG =====
st.set_page_config("Solace AI - Mental Health Chatbot", layout="centered")
openai.api_key = st.secrets["OPENAI_API_KEY"]
USER_FILE = "users.json"

# ===== SESSION STATE INIT =====
if "page" not in st.session_state:
    st.session_state.page = "login"
if "auth" not in st.session_state:
    st.session_state.auth = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat" not in st.session_state:
    st.session_state.chat = []

# ===== USER MANAGEMENT =====
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# ===== CHATBOT REPLY =====
def get_reply(user_input):
    messages = [
        {"role": "system", "content": (
            "You're Solace AI, a supportive and friendly chatbot. "
            "If the user shares emotions, offer empathy, a quote, and calming exercise. "
            "If the user chats casually, reply casually like a close friend with emojis."
        )},
        {"role": "user", "content": user_input}
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()

# ===== SIGNUP PAGE =====
def signup_page():
    st.title("📝 Sign Up to Solace AI")
    new_user = st.text_input("Choose a Username")
    new_pass = st.text_input("Choose a Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        users = load_users()
        if not new_user or not new_pass or not confirm:
            st.warning("Please fill all fields.")
        elif new_user in users:
            st.error("Username already exists. Try logging in.")
        elif new_pass != confirm:
            st.error("Passwords do not match.")
        else:
            users[new_user] = new_pass
            save_users(users)
            st.success("✅ Signup successful! Please log in.")
            st.session_state.page = "login"

# ===== LOGIN PAGE =====
def login_page():
    st.title("🔐 Login to Solace AI")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()
        if username in users and users[username] == password:
            st.session_state.auth = True
            st.session_state.username = username
            st.session_state.chat = []
            st.success("✅ Logged in successfully!")
        else:
            st.error("Invalid credentials. Please try again or Sign up.")

# ===== CHAT PAGE =====
def chat_ui():
    st.markdown("<h2 style='color:#6a1b9a;'>🧠 Solace AI - Mental Health Support</h2>", unsafe_allow_html=True)
    st.caption("Talk to me like a friend. I’m here to support your emotional wellbeing. 💜")

    for sender, msg in st.session_state.chat:
        align = "right" if sender == "user" else "left"
        color = "#e1bee7" if sender == "user" else "#bbdefb"
        text_color = "#000000"
        st.markdown(
            f"<div style='text-align:{align}; background-color:{color}; color:{text_color}; "
            f"padding:10px; border-radius:10px; margin:5px; max-width:70%;'>{msg}</div>",
            unsafe_allow_html=True
        )

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message", key="chat_input", placeholder="Type your message here and press Enter")
        send_btn = st.form_submit_button("Send 💬")

        if send_btn:
            user_msg = user_input.strip()
            if user_msg:
                st.session_state.chat.append(("user", user_msg))
                reply = get_reply(user_msg)
                st.session_state.chat.append(("bot", reply))

    if st.button("Logout"):
        st.session_state.auth = False
        st.session_state.page = "login"
        st.success("👋 Logged out successfully.")

# ===== APP FLOW =====
if not st.session_state.auth:
    st.sidebar.title("🔑 Welcome to Solace AI")
    option = st.sidebar.radio("Navigate:", ["Login", "Sign Up"])

    if option == "Login":
        login_page()
    else:
        signup_page()
else:
    chat_ui()
