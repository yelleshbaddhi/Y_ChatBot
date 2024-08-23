from flask import Flask, render_template, request, jsonify
import google.generativeai as ai
import re

app = Flask(__name__)

# Configure the AI model
API_KEY = 'AIzaSyCnBw0MB4Pm-hwgELTR27OhAT4fpzgEdMA'
ai.configure(api_key=API_KEY)

model = ai.GenerativeModel("gemini-pro")
chat = model.start_chat()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    message = request.form['message']

    # Handle questions related to the name
    name_patterns = [
        r'what is your name',
        r'what are your names',
        r'who are you',
        r'tell me your name',
        r'what should i call you',
        r'what\'s your name',
        r'what is your name\?'
    ]

    # Handle questions related to the developer
    developer_patterns = [
        r'who developed you',
        r'who created you',
        r'who made you',
        r'who is your developer',
        r'who is your creator'
    ]

    # Handle questions related to the chatbot's "father"
    father_patterns = [
        r'who is your father',
        r'who\'s your father',
        r'who is your dad',
        r'who\'s your dad',
        r'do you have a father',
        r'do you have a dad'
    ]

    if any(re.search(pattern, message.lower()) for pattern in name_patterns):
        response_text = 'I am Y_ChatBot, a multimodal AI model.'
    elif any(re.search(pattern, message.lower()) for pattern in developer_patterns):
        response_text = 'I was developed by a team of engineers and researchers.'
    elif any(re.search(pattern, message.lower()) for pattern in father_patterns):
        response_text = 'I do not have a father. I was created by a team of engineers and researchers.'
    else:
        response = chat.send_message(message)
        response_text = response.text

        # Replace "Gemini" or "Bard" with "CA AI ChatBot" in the response
        response_text = re.sub(r'\b(Gemini|Bard)\b', 'Y_ChatBot', response_text)

    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True)
