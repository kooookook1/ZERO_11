from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

# --- Configuration ---
# To use a real LLM, set the following environment variables in a .env file
# LLM_ENDPOINT=your_llm_api_endpoint
# LLM_API_KEY=your_llm_api_key
# LLM_MODEL=the_model_name_you_want_to_use
LLM_ENDPOINT = os.getenv('LLM_ENDPOINT')
LLM_API_KEY = os.getenv('LLM_API_KEY')
LLM_MODEL = os.getenv('LLM_MODEL')

def get_llm_response(user_message):
    """
    This function sends a request to a real LLM API.
    It expects an OpenAI-compatible API endpoint.
    """
    headers = {
        'Authorization': f'Bearer {LLM_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': LLM_MODEL,
        'messages': [{'role': 'user', 'content': user_message}]
    }
    response = requests.post(LLM_ENDPOINT, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def get_joke_response():
    """
    This is the default fallback function.
    It calls the public Joke API.
    """
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    response.raise_for_status()
    joke_data = response.json()
    return f"{joke_data['setup']} - {joke_data['punchline']}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message received'}), 400

    try:
        # If an LLM endpoint is configured, use it.
        # Otherwise, fall back to the Joke API.
        if LLM_ENDPOINT and LLM_API_KEY and LLM_MODEL:
            ai_response = get_llm_response(user_message)
        else:
            ai_response = get_joke_response()

        return jsonify({'response': ai_response})

    except requests.exceptions.RequestException as e:
        print(f"Error calling external API: {e}")
        return jsonify({'error': 'Failed to get a response from the external API.'}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500

if __name__ == '__main__':
    # Default to port 5000 if not specified
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
