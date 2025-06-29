import streamlit as st
import openai
import os
import json

# Setup
st.set_page_config("Solace AI - Mental Health Chatbot", layout="centered")
openai.api_key = st.secrets["OPENAI_API_KEY"]
USER_FILE = "users.json"

# Initialize session state
if "auth" not in st.session_state:
    st.session_state.auth = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "chat" not in st.session_state:
    st.session_state.chat = []

# Load/Save Users
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# GPT reply function
def get_reply(user_input):
    messages = [
        {"role": "system", "content": (
            "You are Solace AI, a warm, friendly mental health chatbot. "
            "If user shares emotional content, respond with empathy, a quote, and a calming tip. "
            "If it's a casual message, chat like a friend using emojis."
        )},
        {"role": "user", "content": user_input}
    ]
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Signup Page
def signup_page():
    st.title("📝 Sign Up to Solace AI")
    new_user = st.text_input("Create a Username")
    new_pass = st.text_input("Create a Password", type="password")
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
            st.success("✅ Signup successful! Please login.")
            st.session_state.signup_success = True

# Login Page
def login_page():
    st.title("🔐 Login to Solace AI")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()
        if user in users and users[user] == pwd:
            st.session_state.auth = True
            st.session_state.username = user
            st.session_state.chat = []
            st.success("✅ Logged in successfully!")
        else:
            st.error("Invalid credentials. Please check or Sign Up.")

# Chat UI
def chat_page():
    st.markdown("<h2 style='color:#6a1b9a;'>💬 Solace AI - Mental Health Support</h2>", unsafe_allow_html=True)
    st.caption("Talk to me like a friend. I’m here for your emotional wellbeing 💜")

    for sender, msg in st.session_state.chat:
        align = "right" if sender == "user" else "left"
        color = "#fce4ec" if sender == "user" else "#e8f5e9"
        st.markdown(
            f"<div style='text-align:{align}; background-color:{color}; padding:10px; "
            f"border-radius:10px; margin:5px; max-width:70%; color:#000;'>{msg}</div>",
            unsafe_allow_html=True
        )

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message", key="chat_input", placeholder="Type and press Enter")
        submitted = st.form_submit_button("Send")

        if submitted and user_input.strip():
            message = user_input.strip()
            st.session_state.chat.append(("user", message))
            reply = get_reply(message)
            st.session_state.chat.append(("bot", reply))

    if st.button("Logout 🚪"):
        st.session_state.auth = False
        st.session_state.username = ""
        st.session_state.chat = []
        st.success("Logged out successfully!")

# Main App
def main():
    st.sidebar.title("🌿 Welcome to Solace AI")
    if not st.session_state.auth:
        page = st.sidebar.radio("Select:", ["Login", "Sign Up"])
        if page == "Login":
            login_page()
        else:
            signup_page()
    else:
        chat_page()

main()
