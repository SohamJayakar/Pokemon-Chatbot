from flask import Flask, render_template, request, jsonify, url_for
from pokemon_chatbot import PokemonChatbot
import os

app = Flask(__name__, static_url_path='/static')
chatbot = PokemonChatbot()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = chatbot.generate_response(user_message, for_cli=False)
    return jsonify({'response': response})

if __name__ == '__main__':
    # Use environment variable for port with a default value
    port = int(os.environ.get('PORT', 5000))
    # In production, debug should be False
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug) 