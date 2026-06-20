from flask import Flask, request, jsonify
from deep_translator import GoogleTranslator

app = Flask(__name__)


@app.route('/')
def home():
    # Serve the existing index.html from the project root (no templates folder needed)
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json(silent=True) or {}
    text = (data.get('text') or '').strip()
    source = data.get('source') or 'auto'
    target = data.get('target') or 'en'

    if not text:
        return jsonify({'error': 'Text is empty.'}), 400

    try:
        translated = GoogleTranslator(source=source, target=target).translate(text)
        return jsonify({'translated': translated})
    except Exception:
        # Avoid leaking internal errors to the client
        return jsonify({'error': 'Translation failed. Please try again.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
