from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import re

app = Flask(__name__)
CORS(app)

# Emotion labels mapping
EMOTION_LABELS = {
    0: "sadness",
    1: "happiness",
    2: "love",
    3: "anger",
    4: "fear",
    5: "surprise"
}

# Load and preprocess data
def load_data():
    try:
        train_data = pd.read_csv('training.csv')
        return train_data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Simple keyword-based emotion analysis
def analyze_text(text):
    # Define emotion keywords
    emotion_keywords = {
        "sadness": ["sad", "unhappy", "depressed", "miserable", "gloomy", "heartbroken"],
        "happiness": ["happy", "joy", "delighted", "pleased", "glad", "cheerful"],
        "love": ["love", "adore", "care", "affection", "fond", "cherish"],
        "anger": ["angry", "mad", "furious", "rage", "annoyed", "irritated"],
        "fear": ["fear", "scared", "afraid", "terrified", "anxious", "worried"],
        "surprise": ["surprise", "shocked", "amazed", "astonished", "unexpected"]
    }
    
    # Convert text to lowercase
    text = text.lower()
    
    # Count matches for each emotion
    emotion_scores = {emotion: 0 for emotion in emotion_keywords}
    
    for emotion, keywords in emotion_keywords.items():
        for keyword in keywords:
            emotion_scores[emotion] += len(re.findall(r'\b' + keyword + r'\b', text))
    
    # Get the dominant emotion
    max_score = max(emotion_scores.values())
    if max_score == 0:
        dominant_emotion = "neutral"
    else:
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
    
    # Calculate probabilities
    total_score = sum(emotion_scores.values())
    if total_score == 0:
        probabilities = {emotion: 1/len(emotion_scores) for emotion in emotion_scores}
    else:
        probabilities = {emotion: score/total_score for emotion, score in emotion_scores.items()}
    
    return dominant_emotion, probabilities

@app.route('/api/analyze', methods=['POST'])
def analyze_emotion():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        emotion, probabilities = analyze_text(text)
        
        return jsonify({
            'emotion': emotion,
            'probabilities': probabilities,
            'text': text
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000) 