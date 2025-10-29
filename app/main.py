from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    # Simulate an AI response
    if user_message:
        ai_response = f"This is a simulated response to: '{user_message}'"
        return jsonify({'response': ai_response})

    return jsonify({'error': 'No message received'}), 400

if __name__ == '__main__':
    app.run(debug=True)
