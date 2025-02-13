import os
import ast
import logging
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure Gemini API
genai.configure(api_key='AIzaSyBCedpSFcr_YxakJftW0jWMtP44jBMnms4')

def parse_python_code(code):
    """Parse Python code and extract basic information."""
    try:
        tree = ast.parse(code)
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
        logging.error(f"Error parsing Python code: {str(e)}")
        return None

def extract_code_structure(code, language):
    """Extract code structure based on the programming language."""
    if language == 'python':
        return parse_python_code(code)

    # For other languages, we'll let the AI model handle the structure analysis
    # This is a simplified approach since parsing other languages would require additional dependencies
    return {
        "language": language,
        "code": code
    }

def generate_documentation(code, language='python'):
    """Generate documentation using Google's Gemini API."""
    try:
        # Get code structure based on language
        code_structure = extract_code_structure(code, language)

        if not code_structure:
            return "Error: Unable to parse the code"

        # Configure the model
        model = genai.GenerativeModel('gemini-pro')

        # Prepare language-specific prompt
        if language == 'python':
            prompt = f"""Generate comprehensive documentation for the following Python code.
            Include:
            1. Overview
            2. Dependencies
            3. Classes and methods documentation
            4. Usage examples

            Code structure:
            Classes: {code_structure.get('classes', [])}
            Functions: {code_structure.get('functions', [])}
            Imports: {code_structure.get('imports', [])}

            Code:
            {code}

            Provide the documentation in Markdown format."""
        else:
            prompt = f"""Generate comprehensive documentation for the following {language.upper()} code.
            Include:
            1. Overview and purpose
            2. Code structure analysis
            3. Key components documentation
            4. Usage examples and best practices

            Code:
            {code}

            Please analyze the code structure, identify major components (classes, functions, methods),
            and provide detailed documentation in Markdown format."""

        # Generate response
        response = model.generate_content(prompt)

        if response.text:
            return response.text
        else:
            return "Error: No documentation generated"

    except Exception as e:
        logging.error(f"Error generating documentation: {str(e)}")
        return f"Error generating documentation: {str(e)}"