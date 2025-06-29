import streamlit as st
import openai
import json
import os

# ========== CONFIGURATION ==========
st.set_page_config("Solace AI Chatbot", layout="centered")
openai.api_key = st.secrets["OPENAI_API_KEY"]
USERS_FILE = "users.json"

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
body { background-color: #f7f2fc; }
.title { text-align: center; font-size: 2.5em; color: #6a1b9a; font-weight: bold; }
.subtitle { text-align: center; color: #555; margin-bottom: 15px; font-style: italic; }
.message {
    padding: 10px 15px; border-radius: 10px; margin: 10px 0; font-size: 15px;
    max-width: 80%; word-wrap: break-word;
    box-shadow: 1px 2px 6px rgba(0,0,0,0.08);
}
.user { background: #ffecf2; color: #8e005e; margin-left: auto; text-align: right; }
.bot { background: #e0f7fa; color: #01579b; margin-right: auto; text-align: left; }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE ==========
if "auth" not in st.session_state: st.session_state.auth = False
if "page" not in st.session_state: st.session_state.page = "Login"
if "username" not in st.session_state: st.session_state.username = ""
if "chat" not in st.session_state: st.session_state.chat = []
if "show_chatbot" not in st.session_state: st.session_state.show_chatbot = False
if "feedback_msg" not in st.session_state: st.session_state.feedback_msg = ""

# ========== USER HANDLING ==========
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ========== CHATBOT ==========
def get_chatbot_reply(user_input):
    messages = [
        {"role": "system", "content": (
            "You are Solace AI, a friendly, chill chatbot for mental health support. "
            "If the user expresses emotions or struggles, respond with empathy, motivational quotes, or calming tips. "
            "If user chats casually, just respond like a close friend with emojis in Tenglish (Telugu + English style)."
        )},
        {"role": "user", "content": user_input}
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.8
    )
    return response.choices[0].message.content.strip()

# ========== SIGNUP ==========
def signup_page():
    st.title("📝 Create Account")
    with st.form("signup_form"):
        uname = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")

        if submit:
            users = load_users()
            if not uname or not pwd or not confirm:
                st.warning("Please fill all fields.")
            elif pwd != confirm:
                st.error("Passwords don’t match.")
            elif uname in users:
                st.error("Username already exists.")
            else:
                users[uname] = pwd
                save_users(users)
                st.session_state.page = "Login"
                st.session_state.feedback_msg = "🎉 Signup successful! Please login."
                st.experimental_rerun()

# ========== LOGIN ==========
def login_page():
    st.title("🔐 Login to Solace AI")
    if st.session_state.feedback_msg:
        st.success(st.session_state.feedback_msg)
        st.session_state.feedback_msg = ""
    with st.form("login_form"):
        uname = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        login = st.form_submit_button("Login")

        if login:
            users = load_users()
            if uname in users and users[uname] == pwd:
                st.session_state.auth = True
                st.session_state.username = uname
                st.session_state.page = "Dashboard"
                st.success(f"Welcome back, {uname}! 🫶")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password. Try again or Sign up.")

# ========== DASHBOARD ==========
def dashboard():
    st.title("🌿 Solace AI Dashboard")
    st.markdown(f"Hello, **{st.session_state.username}** 👋")
    st.markdown("Click below to start chatting:")
    if st.button("💬 Start Chat"):
        st.session_state.show_chatbot = True
        st.experimental_rerun()

# ========== CHATBOT PAGE ==========
def chat_page():
    st.markdown("<h1 class='title'>Solace AI 💜</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Your personal support buddy ✨</p>", unsafe_allow_html=True)

    # Display previous chat
    for role, msg in st.session_state.chat:
        css = "user" if role == "user" else "bot"
        st.markdown(f"<div class='message {css}'>{msg}</div>", unsafe_allow_html=True)

    # Input box
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message 👇", key="chat_input")
        send = st.form_submit_button("Send")

        if send and user_input.strip():
            st.session_state.chat.append(("user", user_input))
            with st.spinner("Thinking... 🤔"):
                reply = get_chatbot_reply(user_input)
            st.session_state.chat.append(("bot", reply))
            st.experimental_rerun()

    # Sidebar
    st.sidebar.title("🔐 Account")
    st.sidebar.markdown(f"**Logged in as:** {st.session_state.username}")
    if st.sidebar.button("🚪 Logout"):
        for key in st.session_state.keys():
            st.session_state[key] = False if isinstance(st.session_state[key], bool) else ""
        st.session_state.page = "Login"
        st.session_state.chat = []
        st.session_state.feedback_msg = "👋 You’ve been logged out."
        st.experimental_rerun()

# ========== ROUTING ==========
if not st.session_state.auth:
    st.sidebar.title("Navigation")
    st.session_state.page = st.sidebar.radio("Choose Page", ["Login", "Sign Up"])
    if st.session_state.page == "Login":
        login_page()
    else:
        signup_page()
elif st.session_state.show_chatbot:
    chat_page()
else:
    dashboard()
