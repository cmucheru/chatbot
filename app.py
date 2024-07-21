from flask import Flask, request, jsonify
import spacy
from spacy.matcher import Matcher

# Initialize Flask app
app = Flask(__name__)

# Load spaCy model and matcher
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)

# Define patterns for greeting and inquiry
greeting_patterns = [
    [{"LOWER": "hello"}],
    [{"LOWER": "hi"}],
    [{"LOWER": "hey"}],
    [{"LOWER": "good"}, {"LOWER": {"IN": ["morning", "afternoon", "evening"]}}]
]

inquiry_patterns = [
    [{"LOWER": {"IN": ["what", "how", "can"]}}, {"LOWER": {"IN": ["you", "I"]}}, {"LOWER": {"IN": ["do", "help", "assist"]}}, {"LOWER": "?"}]
]

# Add patterns to matcher
for pattern in greeting_patterns:
    matcher.add("GREETING", [pattern])

for pattern in inquiry_patterns:
    matcher.add("INQUIRY",[pattern])

# Define response generator
def generate_response(doc):
    matches = matcher(doc)
    for match_id, start, end in matches:
        if nlp.vocab.strings[match_id] == "GREETING":
            return "Hello! How can I assist you today?"
        elif nlp.vocab.strings[match_id] == "INQUIRY":
            return "I can provide information about our services. How can I help you?"

    return "Sorry, I didn't understand that."

# Define route for chatbot endpoint
@app.route('/api/chatbot', methods=['POST'])
def chatbot_response():
    data = request.json
    message = data['message']

    # Process message using spaCy
    doc = nlp(message)
    response = generate_response(doc)

    return jsonify({'message': response})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
