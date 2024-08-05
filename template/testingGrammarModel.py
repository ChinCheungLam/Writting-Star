from flask import Flask, request, jsonify, send_from_directory
import os
import openai
from dotenv import load_dotenv

# Load the environment variables from the .env file
dotenv_path = '/Users/cclam/Desktop/CSS495 Capstone/GTP3Key/key.env'
load_dotenv(dotenv_path)

app = Flask(__name__, static_folder='public')

def generate_grammar_correction(paragraph, model):
    try:
        response = openai.Completion.create(
            model=model,
            prompt=f"Correct the grammar in the following paragraph:\n\n{paragraph}\n\nCorrected paragraph:",
            max_tokens=500,
            stop=["\n\n"]
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating grammar correction: {e}")
        return None

@app.route('/correct-grammar', methods=['POST'])
def correct_grammar():
    data = request.json
    paragraph = data.get('paragraph', '')
    if not paragraph:
        return jsonify({'error': 'No paragraph provided'}), 400

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify({'error': 'API key not found'}), 500

    openai.api_key = api_key
    fine_tuned_model = "ft:davinci-002:personal::9lywO8iv"

    correction = generate_grammar_correction(paragraph, fine_tuned_model)
    return jsonify({'correction': correction})

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/', methods=['GET'])
def index():
    return send_from_directory(app.static_folder, 'grammarChecking&Correction.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
