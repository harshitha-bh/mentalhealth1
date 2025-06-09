import random, json
from textblob import TextBlob

def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity

def pick_quote(emotion):
    with open('quotes.json') as f: quotes = json.load(f)
    return random.choice(quotes.get(emotion, ["You're not alone."]))

def pick_exercise(emotion):
    with open('exercises.json') as f: ex = json.load(f)
    return random.choice(ex.get(emotion, ["Take a few deep breaths now."]))
