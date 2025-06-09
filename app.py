import streamlit as st
from streamlit_chat import message
import openai
import datetime
import sqlite3
from utils import analyze_sentiment, pick_quote, pick_exercise

openai.api_key = st.secrets["OPENAI_API_KEY"]
DB = "data/sessions.db"

def init_db():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS sessions(user,ts,emotion,quote,exercise)")
    conn.commit(); conn.close()

def log_session(user, emotion, quote, exercise):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("INSERT INTO sessions VALUES (?,?,?,?,?)", (user, datetime.datetime.now(), emotion, quote, exercise))
    conn.commit(); conn.close()

def get_mood_history(user):
    import pandas as pd
    conn = sqlite3.connect(DB)
    df = pd.read_sql("SELECT ts,emotion FROM sessions WHERE user=? ORDER BY ts", conn, params=(user,))
    return df

def main():
    st.title("💬 Mental Health Chatbot")
    init_db()

    if "user" not in st.session_state:
        st.session_state.user = st.text_input("Enter your name to begin")
        if not st.session_state.user:
            st.stop()

    st.sidebar.write(f"Hello, **{st.session_state.user}**")
    df = get_mood_history(st.session_state.user)
    if not df.empty:
        import altair as alt
        chart = alt.Chart(df).mark_line().encode(x='ts:T', y='emotion:Q')
        st.sidebar.altair_chart(chart, use_container_width=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        message(msg["content"], is_user=msg["role"]=="user")

    user_input = st.text_input("How are you feeling today?", key="input")
    if user_input:
        st.session_state.messages.append({"role":"user","content":user_input})
        emotion_score = analyze_sentiment(user_input)
        emotion = "sad" if emotion_score < -0.2 else "anxious" if emotion_score<0 else "neutral"
        quote = pick_quote(emotion)
        exercise = pick_exercise(emotion)
        prompt = f"User feels {emotion}. Provide empathic response including quote '{quote}' and exercise '{exercise}'."
        resp = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role":"user","content":prompt}])
        reply = resp.choices[0].message.content
        st.session_state.messages.append({"role":"assistant","content":reply})
        log_session(st.session_state.user, emotion_score, quote, exercise)

        # breathing widget
        if "breathing" in exercise.lower():
            st.balloons(); st.write("Try breathing with me...")
            st.progress(0)
            import time
            for i in range(100): time.sleep(0.05); st.progress(i+1)

    st.sidebar.subheader("Recent Quotes")
    for q in list(st.session_state.messages)[-5:]:
        if q["role"]=="assistant": st.sidebar.write(f"> {q['content'].splitlines()[0]}")

if __name__=="__main__":
    main()
