# Emotion Analysis API

This is a Flask-based API that analyzes emotions in text using machine learning. The API uses a trained model to classify text into six emotional categories: sadness, happiness, love, anger, fear, and surprise.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### 1. Analyze Emotion
- **Endpoint**: `/api/analyze`
- **Method**: POST
- **Content-Type**: application/json
- **Request Body**:
```json
{
    "text": "Your text to analyze"
}
```
- **Response**:
```json
{
    "emotion": "happiness",
    "probabilities": {
        "sadness": 0.1,
        "happiness": 0.6,
        "love": 0.1,
        "anger": 0.05,
        "fear": 0.1,
        "surprise": 0.05
    },
    "text": "Your text to analyze"
}
```

### 2. Health Check
- **Endpoint**: `/api/health`
- **Method**: GET
- **Response**:
```json
{
    "status": "healthy"
}
```

## Integration with Frontend

To integrate with your frontend application:

1. The API has CORS enabled, so you can make requests from any origin
2. Use the following fetch example to make requests:

```javascript
const response = await fetch('http://localhost:5000/api/analyze', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        text: 'Your text to analyze'
    })
});
const data = await response.json();
```

## Error Handling

The API returns appropriate error messages with corresponding HTTP status codes:
- 400: Bad Request (missing or invalid input)
- 500: Internal Server Error (server-side issues)

## Model Training

The model is automatically trained on first run using the provided training data. The trained model is saved to disk for subsequent uses. If you want to retrain the model, simply delete the `model.pkl` and `vectorizer.pkl` files. 