import streamlit as st
import openai
import os
import json

# Load or initialize user database
USER_FILE = "users.json"
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

# Load users
def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

# Save users
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# Initialize OpenAI
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize session state
defaults = {
    "auth": False,
    "username": "",
    "page": "Login",
    "users": load_users(),
    "chat_history": [],
    "show_chatbot": False
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# CSS for chat styling
st.set_page_config("Solace AI")
st.markdown("""
<style>
.title { text-align:center; font-size:2.2em; color:#6a1b9a; font-weight:bold; }
.subtitle { text-align:center; font-size:1.1em; color:#444; font-style:italic; }
.message {
    padding: 10px 14px; border-radius: 10px; margin: 8px 0;
    font-size: 15px; max-width: 80%; word-wrap: break-word;
}
.user { background-color: #fce4ec; color: #880e4f; text-align: right; margin-left: auto; }
.bot { background-color: #e3f2fd; color: #0d47a1; text-align: left; margin-right: auto; }
</style>
""", unsafe_allow_html=True)

# Chatbot logic using chat history
def get_chatbot_reply():
    messages = [
        {"role": "system", "content": (
            "You are Solace AI, a kind, casual, friendly mental health support chatbot. "
            "Use emojis and friendly tone. If user shares emotional feelings, respond with warmth, quotes, and calming advice. "
            "If they chat normally, respond like a close friend casually."
        )}
    ]
    for sender, message in st.session_state.chat_history:
        role = "user" if sender == "user" else "assistant"
        messages.append({"role": role, "content": message})

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

# --- Login Page ---
def login_page():
    st.title("🔐 Login to Solace AI")
    with st.form("login_form", clear_on_submit=True):
        uname = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        login_btn = st.form_submit_button("Login")
        if login_btn:
            if uname in st.session_state.users and st.session_state.users[uname] == pwd:
                st.success(f"🎉 Logged in successfully! Welcome, {uname}")
                st.session_state.auth = True
                st.session_state.username = uname
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error("❌ Invalid username or password. Please sign up if you're new.")

# --- Signup Page ---
# --- Signup Page ---
def signup_page():
    st.title("📝 Sign Up for Solace AI")

    # Maintain signup state flags
    if "signup_success" not in st.session_state:
        st.session_state.signup_success = False
    if "signup_error" not in st.session_state:
        st.session_state.signup_error = ""

    with st.form("signup_form", clear_on_submit=True):
        uname = st.text_input("Choose a Username")
        pwd = st.text_input("Password", type="password")
        confirm_pwd = st.text_input("Confirm Password", type="password")
        signup_btn = st.form_submit_button("Sign Up")

        if signup_btn:
            if not uname or not pwd or not confirm_pwd:
                st.session_state.signup_error = "Please fill all fields."
                st.session_state.signup_success = False
            elif uname in st.session_state.users:
                st.session_state.signup_error = "⚠️ Username already exists."
                st.session_state.signup_success = False
            elif pwd != confirm_pwd:
                st.session_state.signup_error = "⚠️ Passwords do not match."
                st.session_state.signup_success = False
            else:
                st.session_state.users[uname] = pwd
                save_users(st.session_state.users)
                st.session_state.signup_success = True
                st.session_state.signup_error = ""

    # Show messages AFTER form submit
    if st.session_state.signup_success:
        st.success("🎉 Signed up successfully! Please login to continue.")
        if st.button("Go to Login"):
            st.session_state.page = "Login"
            st.rerun()

    elif st.session_state.signup_error:
        st.error(st.session_state.signup_error)


# --- Dashboard Page ---
def dashboard():
    st.title(f"👋 Welcome, {st.session_state.username}")
    st.markdown("You’re logged in to **Solace AI**, your mental health buddy 💗")
    if st.button("💬 Start Chat"):
        st.session_state.show_chatbot = True
        st.rerun()

# --- Chat Page ---
def chat_page():
    st.markdown("<h1 class='title'>🌿 Solace AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>I'm here as your mental health companion & friend 🤗</p>", unsafe_allow_html=True)

    # Display chat history
    for sender, message in st.session_state.chat_history:
        role_class = "user" if sender == "user" else "bot"
        st.markdown(f"<div class='message {role_class}'>{message}</div>", unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message", label_visibility="collapsed")
        send_btn = st.form_submit_button("Send")
        if send_btn and user_input.strip():
            st.session_state.chat_history.append(("user", user_input))
            with st.spinner("Solace is typing..."):
                bot_reply = get_chatbot_reply()
            st.session_state.chat_history.append(("bot", bot_reply))
            st.rerun()

    # Logout option
    st.sidebar.title("🔒 Account")
    st.sidebar.write(f"👤 Logged in as: `{st.session_state.username}`")
    if st.sidebar.button("Logout"):
        for key in ["auth", "username", "page", "show_chatbot", "chat_history"]:
            st.session_state[key] = False if isinstance(st.session_state[key], bool) else ""
        st.rerun()

# --- Routing Logic ---
if not st.session_state.auth:
    st.sidebar.title("Access")
    st.session_state.page = st.sidebar.radio("Go to", ["Login", "Sign Up"])
    if st.session_state.page == "Login":
        login_page()
    else:
        signup_page()
elif st.session_state.show_chatbot:
    chat_page()
else:
    dashboard()
