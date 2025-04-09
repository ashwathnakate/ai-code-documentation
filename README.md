# 📝 Code Documentation Generator Web App 🚀

This project is a Flask-based web application that allows users to upload code files in Python, Java, C++, or JavaScript and generates automated documentation for the uploaded code.

---

## 📂 Project Structure

```
project-root/
│
├── __pycache__/               # 🐍 Compiled Python files
│
├── static/                    # 📁 Static assets
│   ├── css/                   # 🎨 CSS files for styling
│   └── js/                    # ⚡ JavaScript files for interactivity
│
├── templates/                 # 🖼️ HTML templates
│   ├── base.html              # 🏗️ Base template with common layout
│   └── index.html             # 📝 Main template with file upload form
│
├── .replit                    # ⚙️ Replit configuration file
│
├── app.py                     # 🛠️ Main Flask application
│
├── doc_generator.py           # 📄 Script for generating code documentation
│
├── generated-icon.png         # 🖼️ Project icon/image
│
├── main.py                    # 🐍 (Optional) Additional entry point or script
│
├── package-lock.json          # 📦 NPM lock file for JavaScript dependencies
│
├── package.json               # 📋 NPM project metadata
│
├── pyproject.toml             # 📝 Python project metadata
│
├── replit.nix                 # 🛡️ Replit environment configuration
│
└── uv.lock                    # 🔒 Lock file for Python dependencies
```

---

## ✨ Features

- 🔄 **Upload Code Files**: Supports Python, Java, C++, and JavaScript.
- 📜 **Automatic Documentation**: Generates documentation based on the code content and language.
- 🔒 **Secure File Handling**: Uses `werkzeug` for secure file uploads.
- 🐛 **Logging**: Built-in logging for error tracking and debugging.
- 📏 **File Size Limit**: Maximum upload size set to 1MB.
- 🎨 **Dynamic Templates**: Utilizes Jinja2 templates for dynamic HTML rendering.

---

## 🛠️ Installation and Usage

### 1. 📥 Clone the Repository
```bash
git clone https://github.com/your-username/code-doc-generator.git
cd code-doc-generator
```

### 2. 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. 🚀 Run the Application
```bash
python app.py
```

The app will be accessible at `http://0.0.0.0:5000`.

---

## 🔗 API Endpoints

- **/** : 🏡 Home route to render the upload form.
- **/upload** : 📤 POST route to handle file uploads and return generated documentation.

---

## 🔑 Environment Variables

- `FLASK_SECRET_KEY`: Secret key for Flask sessions (default: `dev_key_123`).

---

## 🔮 Future Enhancements

- 🌍 Support for more programming languages.
- 🛡️ Enhanced code analysis and documentation generation.
- ☁️ Integration with cloud storage for handling larger files.

---

## 🖼️ Screenshots
![Sample1](<to use1.JPG>)

![Sample2](<to use2.JPG>)
---

## 🤝 Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

Happy coding! 🚀🎉

---

Developed by [Github Link](https://github.com/ashwathnakate)
