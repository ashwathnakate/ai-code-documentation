import os
import ast
import logging
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

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
    """Generate documentation using OpenAI API."""
    try:
        # Parse code structure
        code_structure = parse_python_code(code)
        
        if not code_structure:
            return "Error: Unable to parse the code"

        # Prepare prompt for OpenAI
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

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a Python documentation expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000
        )

        return response.choices[0].message.content

    except Exception as e:
        logging.error(f"Error generating documentation: {str(e)}")
        return f"Error generating documentation: {str(e)}"
