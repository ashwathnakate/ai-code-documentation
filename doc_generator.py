import os
import ast
import logging
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure Gemini API
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def parse_python_code(code):
    """Parse Python code and extract basic information."""
    try:
        tree = ast.parse(code)

        # Extract basic code structure
        classes = []
        functions = []
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.Import):
                imports.extend(n.name for n in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(f"{node.module}")

        return {
            "classes": classes,
            "functions": functions,
            "imports": imports
        }
    except Exception as e:
        logging.error(f"Error parsing code: {str(e)}")
        return None

def generate_documentation(code):
    """Generate documentation using Google's Gemini API."""
    try:
        # Parse code structure
        code_structure = parse_python_code(code)

        if not code_structure:
            return "Error: Unable to parse the code"

        # Configure the model
        model = genai.GenerativeModel('gemini-pro')

        # Prepare prompt for Gemini
        prompt = f"""Generate comprehensive documentation for the following Python code.
        Include:
        1. Overview
        2. Dependencies
        3. Classes and methods documentation
        4. Usage examples

        Code structure:
        Classes: {code_structure['classes']}
        Functions: {code_structure['functions']}
        Imports: {code_structure['imports']}

        Code:
        {code}

        Provide the documentation in Markdown format."""

        # Generate response
        response = model.generate_content(prompt)

        if response.text:
            return response.text
        else:
            return "Error: No documentation generated"

    except Exception as e:
        logging.error(f"Error generating documentation: {str(e)}")
        return f"Error generating documentation: {str(e)}"