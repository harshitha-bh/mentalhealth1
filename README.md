
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


SIGN UP
 ![signup](https://github.com/harshitha-bh/mentalhealth1/blob/main/images/mental2.png)  
 LOG IN
 ![login](https://github.com/harshitha-bh/mentalhealth1/blob/main/images/mental1.png) 
 CHATBOT
 ![chatbot](https://github.com/harshitha-bh/mentalhealth1/blob/main/images/mental4.png) 

>  real screenshots are placed in the `images/` folder with correct file names above._

---

## 🌐 Live Demo
Start using Solace AI which supports u mentally and it will be a good friend too....(streamlit link is below to use the app)
🔗 https://mentalhealth1-users.streamlit.app/           
Feel better, one message at a time.

---

## 🔐 Prerequisites

- Python 3.7 or higher  
- OpenAI API key → (https://platform.openai.com/account/api-keys)  
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
