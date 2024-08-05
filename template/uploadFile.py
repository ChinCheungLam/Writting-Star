from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import openai
import docx
from dotenv import load_dotenv

# Load the environment variables from the .env file
dotenv_path = '/Users/cclam/Desktop/CSS495 Capstone/GTP3Key/key.env'
load_dotenv(dotenv_path)

# Set the OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'docx'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB limit

app = Flask(__name__, static_folder='public')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_docx(file_path):
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error reading .docx file: {e}")
        return None

def generate_story_outline(prompt, story_size, genre):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate a story outline based on the following details:\n\n"
                                            f"Prompt: {prompt}\n"
                                            f"Story Size: {story_size}\n"
                                            f"Genre: {genre}\n\n"
                                            f"Outline:"}
            ],
            max_tokens=500
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating story outline: {e}")
        return None

def generate_story(prompt, character_details, story_size, genre, narrative_perspective):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate a story based on the following details:\n\n"
                                            f"Prompt: {prompt}\n"
                                            f"Character Details: {character_details}\n"
                                            f"Story Size: {story_size}\n"
                                            f"Genre: {genre}\n"
                                            f"Narrative Perspective: {narrative_perspective}\n\n"
                                            f"Story:"}
            ],
            max_tokens=1000
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error generating story: {e}")
        return None

def continue_story(content):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Continue the following story:\n\n{content}\n\nContinuation:"}
            ],
            max_tokens=500
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error continuing story: {e}")
        return None

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        print(f"File saved at {file_path}")
        print(f"File type: {file.mimetype}")

        file_extension = filename.rsplit('.', 1)[1].lower()
        if file_extension == 'docx':
            content = read_docx(file_path)
            if content is None:
                return jsonify({'error': 'Failed to read .docx file'}), 400
        else:
            with open(file_path, 'r') as f:
                content = f.read()

        return jsonify({'message': 'File successfully uploaded', 'content': content}), 200

    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/generate-outline', methods=['POST'])
def generate_outline():
    data = request.json
    prompt = data.get('prompt', '')
    story_size = data.get('storySize', 'medium')
    genre = data.get('genre', 'fairy-tales')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    outline = generate_story_outline(prompt, story_size, genre)
    if outline:
        return jsonify({'outline': outline}), 200
    else:
        return jsonify({'error': 'Failed to generate story outline'}), 500

@app.route('/generate-story', methods=['POST'])
def generate_story_endpoint():
    data = request.json
    prompt = data.get('prompt', '')
    character_details = data.get('characterDetails', '')
    story_size = data.get('storySize', 'medium')
    genre = data.get('genre', 'fairy-tales')
    narrative_perspective = data.get('narrativePerspective', 'third-person')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    story = generate_story(prompt, character_details, story_size, genre, narrative_perspective)
    if story:
        return jsonify({'story': story}), 200
    else:
        return jsonify({'error': 'Failed to generate story'}), 500

@app.route('/continue-story', methods=['POST'])
def continue_story_endpoint():
    data = request.json
    content = data.get('content', '')

    if not content:
        return jsonify({'error': 'Content is required'}), 400

    continued_story = continue_story(content)
    if continued_story:
        return jsonify({'continuedStory': continued_story}), 200
    else:
        return jsonify({'error': 'Failed to continue the story'}), 500

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/', methods=['GET'])
def index():
    return send_from_directory(app.static_folder, 'grammarChecking&Correction.html')

if __name__ == '__main__':
    app.run(debug=True)
