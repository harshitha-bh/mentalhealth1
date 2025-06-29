import streamlit as st
import openai
import json
import os

# ========== CONFIG ==========
st.set_page_config("Solace AI", layout="centered")
openai.api_key = st.secrets["OPENAI_API_KEY"]
USERS_FILE = "users.json"

# ========== CSS STYLES ==========
st.markdown("""
<style>
.title { text-align: center; font-size: 2.4em; color: #6a1b9a; font-weight: bold; }
.subtitle { text-align: center; color: #444; margin-bottom: 20px; font-style: italic; }
.message {
    padding: 12px 16px; border-radius: 10px; margin: 8px 0; font-size: 15px;
    line-height: 1.5; max-width: 85%; word-wrap: break-word;
    box-shadow: 1px 2px 6px rgba(0,0,0,0.08);
}
.user { background: #ffe0f0; color: #880e4f; margin-left: auto; text-align: right; }
.bot { background: #e1f5fe; color: #01579b; margin-right: auto; text-align: left; }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE INIT ==========
if "auth" not in st.session_state:
    st.session_state.auth = False
if "page" not in st.session_state:
    st.session_state.page = "Login"
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat" not in st.session_state:
    st.session_state.chat = []
if "show_chatbot" not in st.session_state:
    st.session_state.show_chatbot = False

# ========== UTILITIES ==========
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ========== CHATBOT FUNCTION ==========
def get_chatbot_reply(user_input):
    messages = [
        {"role": "system", "content": (
            "You are Solace AI, a friendly mental health chatbot. "
            "When users open up emotionally, respond with empathy, quotes, or calming tips. "
            "When users chat casually, respond like a funny, chill friend using emojis."
        )},
        {"role": "user", "content": user_input}
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

# ========== SIGNUP PAGE ==========
def signup_page():
    st.title("📝 Sign Up for Solace AI")
    with st.form("signup_form", clear_on_submit=True):
        uname = st.text_input("Choose a username")
        pwd = st.text_input("Create a password", type="password")
        confirm = st.text_input("Confirm password", type="password")
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            users = load_users()
            if not uname or not pwd or not confirm:
                st.warning("Please fill out all fields.")
            elif pwd != confirm:
                st.error("Passwords do not match.")
            elif uname in users:
                st.error("Username already exists. Try logging in.")
            else:
                users[uname] = pwd
                save_users(users)
                st.success("🎉 Signup successful! Please log in now.")
                st.session_state.page = "Login"
                st.rerun()

# ========== LOGIN PAGE ==========
def login_page():
    st.title("🔐 Login to Solace AI")
    with st.form("login_form", clear_on_submit=True):
        uname = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            users = load_users()
            if uname in users and users[uname] == pwd:
                st.session_state.auth = True
                st.session_state.username = uname
                st.session_state.page = "Dashboard"
                st.success(f"✅ Login successful! Welcome, {uname} 💜")
                st.rerun()
            else:
                st.error("Invalid username or password.")

# ========== DASHBOARD ==========
def dashboard():
    st.title(f"👋 Welcome, {st.session_state.username}")
    st.markdown("You're now logged in to **Solace AI** 💬")
    if st.button("🧠 Start Chatbot"):
        st.session_state.show_chatbot = True
        st.rerun()

# ========== CHATBOT PAGE ==========
def chat_page():
    st.markdown("<h1 class='title'>🌿 Solace AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>I'm here with you 💗 Let's talk.</p>", unsafe_allow_html=True)

    # Display chat messages
    for role, msg in st.session_state.chat:
        css_class = "user" if role == "user" else "bot"
        st.markdown(f"<div class='message {css_class}'>{msg}</div>", unsafe_allow_html=True)

    # Input for new message
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message", label_visibility="collapsed")
        sent = st.form_submit_button("Send")
        if sent and user_input.strip():
            st.session_state.chat.append(("user", user_input))
            with st.spinner("Solace is typing..."):
                reply = get_chatbot_reply(user_input)
            st.session_state.chat.append(("bot", reply))
            st.rerun()

    # Sidebar for logout
    st.sidebar.title("🔑 Account")
    st.sidebar.markdown(f"Logged in as: **{st.session_state.username}**")
    if st.sidebar.button("Logout"):
        for key in ["auth", "username", "page", "show_chatbot", "chat"]:
            st.session_state[key] = False if isinstance(st.session_state[key], bool) else ""
        st.session_state.chat = []
        st.success("👋 You have been logged out successfully.")
        st.rerun()

# ========== ROUTER ==========
if not st.session_state.auth:
    st.sidebar.title("🔐 Access")
    st.session_state.page = st.sidebar.radio("Go to", ["Login", "Sign Up"])
    login_page() if st.session_state.page == "Login" else signup_page()
elif st.session_state.show_chatbot:
    chat_page()
else:
    dashboard()
