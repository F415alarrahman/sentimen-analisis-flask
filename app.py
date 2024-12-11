from flask import Flask, render_template, request, jsonify, session
from indobert import SentimentAnalyzer
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

model_indobert = 'model/saved_model'
analyzer_indobert = SentimentAnalyzer(model_indobert)

@app.route('/')
def index():
    reviews = session.get('reviews', [])
    return render_template('index.html', reviews=reviews)

@app.route('/sentimen')
def sentimen():
    reviews = session.get('reviews', [])
    
    sentiment_results = []
    for review in reviews:
        predicted_class, probabilities = analyzer_indobert.predict_sentiment(review['text'])
        sentiment = "Positif" if predicted_class == 1 else "Negatif"
        sentiment_results.append({
            "text": review['text'],
            "sentiment": sentiment
        })
    
    return render_template('sentimen.html', sentiment_results=sentiment_results)

@app.route('/add_review', methods=['POST'])
def add_review():
    data = request.json
    review_text = data['text']
    
    reviews = session.get('reviews', [])
    reviews.append({"text": review_text})
    
    session['reviews'] = reviews
    
    return jsonify({"text": review_text})

