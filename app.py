import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import logging
from doc_generator import generate_documentation
import tempfile

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_key_123")

# Configure upload settings
ALLOWED_EXTENSIONS = {'py'}
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only Python files are allowed'}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        with open(filepath, 'r') as f:
            code_content = f.read()

        # Generate documentation
        documentation = generate_documentation(code_content)
        
        # Clean up the temporary file
        os.remove(filepath)

        return jsonify({
            'success': True,
            'documentation': documentation,
            'original_code': code_content
        })

    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        return jsonify({'error': 'Error processing file'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
