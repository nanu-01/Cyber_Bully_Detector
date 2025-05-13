from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Paste your actual API key here
PERSPECTIVE_API_KEY = 'XXXXXXX' #Please put your API Key here
PERSPECTIVE_URL = f'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}'

@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    request_data = {
        'comment': {'text': text},
        'languages': ['en'],
        'requestedAttributes': {'TOXICITY': {}}
    }

    response = requests.post(
        PERSPECTIVE_URL,
        headers={"Content-Type": "application/json"},
        json=request_data
    )

    if response.status_code == 200:
        result = response.json()
        score = result['attributeScores']['TOXICITY']['summaryScore']['value']
        return jsonify({'score': score})
    else:
        print("🔴 Error:", response.status_code, response.text)
        return jsonify({'error': 'API request failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
