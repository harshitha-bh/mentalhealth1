
# 🌿 Solace AI – Your Mental Health Support Chatbot 💬

Welcome to **Solace AI** – a real-time, emotionally aware mental health companion. Built using OpenAI's LLMs and Streamlit, this chatbot is designed to provide supportive, casual, and therapeutic conversations to those in need of a friend, a listener, or just a bit of encouragement.

---

## 🎯 Features

✅ Personalized conversation based on emotional tone  
✅ Real-time reply with single-click experience  
✅ Friendly UI with calm therapy colors 🌸  
✅ Motivational quotes, breathing exercises when needed  
✅ Login & Signup with persistent user storage  
✅ GPT-3.5 Turbo powered natural conversation  
✅ Context-aware replies based on chat history  
✅ Mobile responsive UI with emoji-rich responses  
✅ Secure logout and clear session handling

---

## 🛠 Tech Stack

| Layer     | Technology                         |
|-----------|------------------------------------|
| Frontend  | Streamlit + Embedded CSS           |
| Backend   | Python, OpenAI GPT-3.5 Turbo       |
| Storage   | JSON (`users.json` for auth data)  |
| Hosting   | Streamlit Cloud / Local runtime    |
| Styling   | Custom CSS injected in Streamlit   |
| Model Dev | Google Colab (if extended training)|

---

## 🖼️ Screenshots

| Signup Page | Login Page | Chatbot in Action |
|-------------|------------|-------------------|
| ![signup](images/signup.png) | ![login](images/login.png) | ![chatbot](images/chat.png) |

> _Tip: Place real screenshots in the `images/` folder with correct file names above._

---

## 🌐 Live Demo

🔗 [Click here to try Solace AI](https://your-solace-deployment-link.streamlit.app)  
Feel better, one message at a time.

---

## 🔐 Prerequisites

- Python 3.7 or higher  
- OpenAI API key → [Get from OpenAI](https://platform.openai.com/account/api-keys)  
- `streamlit` and `openai` installed

---

## 🧪 Run This Project Locally

```bash
#Clone the repository
git clone https://github.com/yourusername/solace-ai-chatbot.git
cd solace-ai-chatbot

# Install dependencies
pip install -r requirements.txt

# Add your OpenAI API key
mkdir -p .streamlit
echo "OPENAI_API_KEY = 'your-openai-key-here'" > .streamlit/secrets.toml

# Run the Streamlit app
streamlit run app.py
