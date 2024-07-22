from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
from spacy.matcher import Matcher
from spacy.cli import download

app = Flask(__name__)
CORS(app)

# Ensure the spaCy model is downloaded
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

matcher = Matcher(nlp.vocab)

greeting_patterns = [
    [{"LOWER": "hello"}],
    [{"LOWER": "hi"}],
    [{"LOWER": "hey"}],
    [{"LOWER": "good"}, {"LOWER": {"IN": ["morning", "afternoon", "evening"]}}]
]

inquiry_patterns = [
    [{"LOWER": {"IN": ["what", "how", "can"]}}, {"LOWER": {"IN": ["you", "I"]}}, {"LOWER": {"IN": ["do", "help", "assist"]}}, {"LOWER": "?"}]
]

for pattern in greeting_patterns:
    matcher.add("GREETING", [pattern])

for pattern in inquiry_patterns:
    matcher.add("INQUIRY",[pattern])

def generate_response(doc):
    matches = matcher(doc)
    for match_id, start, end in matches:
        if nlp.vocab.strings[match_id] == "GREETING":
            return "Hello! How can I assist you today?"
        elif nlp.vocab.strings[match_id] == "INQUIRY":
            return "I can provide information about our services. How can I help you?"
    return "Sorry, I didn't understand that."

@app.route('/api/chatbot', methods=['POST'])
def chatbot_response():
    data = request.json
    message = data['message']
    doc = nlp(message)
    response = generate_response(doc)
    return jsonify({'message': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
