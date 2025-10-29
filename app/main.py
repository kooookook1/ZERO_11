from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

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
        # Call the external Joke API
        response = requests.get('https://official-joke-api.appspot.com/random_joke')
        response.raise_for_status()  # Raise an exception for bad status codes

        joke_data = response.json()
        ai_response = f"{joke_data['setup']} - {joke_data['punchline']}"

        return jsonify({'response': ai_response})

    except requests.exceptions.RequestException as e:
        print(f"Error calling Joke API: {e}")
        return jsonify({'error': 'Failed to get a response from the Joke API.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
