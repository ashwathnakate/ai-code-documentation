import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import logging
from doc_generator import generate_documentation
import tempfile
import zipfile
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_key_123")

# Configure upload settings
ALLOWED_EXTENSIONS = {'py', 'java', 'cpp', 'js'}
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_language(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    language_map = {
        'py': 'python',
        'java': 'java',
        'cpp': 'cpp',
        'js': 'javascript'
    }
    return language_map.get(ext)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download-project')
def download_project():
    try:
        # Create a BytesIO object to store the zip file
        memory_file = BytesIO()

        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            # List of directories to include
            dirs_to_include = ['templates', 'static']
            files_to_include = ['app.py', 'doc_generator.py', 'main.py']

            # Add directories
            for dir_name in dirs_to_include:
                for root, dirs, files in os.walk(dir_name):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = file_path  # Keep the directory structure
                        zf.write(file_path, arcname)

            # Add individual files
            for file_name in files_to_include:
                if os.path.exists(file_name):
                    zf.write(file_name)

        # Seek to the beginning of the BytesIO object
        memory_file.seek(0)

        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name='python-doc-generator.zip'
        )

    except Exception as e:
        logging.error(f"Error creating zip file: {str(e)}")
        return jsonify({'error': 'Error creating download package'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed types are: Python, Java, C++, and JavaScript'}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        with open(filepath, 'r') as f:
            code_content = f.read()

        # Get the programming language from file extension
        language = get_file_language(filename)

        # Generate documentation with language context
        documentation = generate_documentation(code_content, language)

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