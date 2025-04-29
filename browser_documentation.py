import os
import sys
import subprocess
import webbrowser
from pathlib import Path
from flask import Flask, render_template, request, jsonify
import markdown
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Define base directory
BASE_DIR = Path(__file__).parent
LEARNING_DIR = BASE_DIR / "learning"

# Define modules and their descriptions
MODULES = {
    "simple": {"path": LEARNING_DIR / "simple", "desc": "Basic MCP examples (stdio and SSE)"},
    "groq": {"path": LEARNING_DIR / "groq", "desc": "Groq LLM integration"},
    "Servers": {"path": LEARNING_DIR / "Servers", "desc": "Various server implementations"},
    "Clients": {"path": LEARNING_DIR / "Clients", "desc": "Advanced client implementations"},
    "Langgraph": {"path": LEARNING_DIR / "langgraph", "desc": "Learning Langgraph"},
    "asyncoronus python": {
        "path": LEARNING_DIR / "asyncoronus python",
        "desc": "Async programming examples",
    },
}

def read_markdown_file(file_path):
    """Read and convert Markdown file to HTML."""
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            return markdown.markdown(content, extensions=['fenced_code', 'tables'])
    return "<p>No documentation found.</p>"

def list_scripts(module_name):
    """List Python scripts in a module directory."""
    module_info = MODULES.get(module_name)
    if not module_info:
        return []
    return [f.name for f in module_info["path"].glob("*.py") if f.is_file()]

@app.route("/")
def home():
    """Render the home page with project overview."""
    readme_path = BASE_DIR / "README.md"
    content = read_markdown_file(readme_path)
    return render_template(
        "index.html",
        content=content,
        modules=MODULES,
        current_module=None
    )

@app.route("/module/<module_name>")
def module(module_name):
    """Render a module's documentation and scripts."""
    if module_name not in MODULES:
        return render_template(
            "error.html",
            message=f"Module '{module_name}' not found.",
            modules=MODULES
        )
    module_info = MODULES[module_name]
    readme_path = module_info["path"] / "README.md"
    content = read_markdown_file(readme_path)
    scripts = list_scripts(module_name)
    return render_template(
        "module.html",
        content=content,
        modules=MODULES,
        current_module=module_name,
        scripts=scripts
    )

@app.route("/run_script", methods=["POST"])
def run_script():
    """Run a script and return its output."""
    module_name = request.form.get("module_name")
    script_name = request.form.get("script_name")
    
    if module_name not in MODULES:
        return jsonify({"error": f"Module '{module_name}' not found."}), 400
    
    module_info = MODULES[module_name]
    script_path = module_info["path"] / script_name
    
    if not script_path.exists() or not script_path.is_file():
        return jsonify({"error": f"Script '{script_name}' not found."}), 400
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=module_info["path"],
            check=True,
            text=True,
            capture_output=True,
            timeout=30  # Prevent hanging
        )
        output = result.stdout
        error = result.stderr if result.stderr else ""
        return jsonify({"output": output, "error": error})
    except subprocess.CalledProcessError as e:
        return jsonify({"output": e.stdout, "error": e.stderr}), 500
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Script execution timed out."}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    # Check dependencies
    try:
        import flask
        import markdown
        import dotenv
    except ImportError:
        print("Error: Required dependencies missing. Please run 'uv pip install -r requirements.txt'.")
        sys.exit(1)
    
    # Check virtual environment
    if not os.getenv("VIRTUAL_ENV"):
        print("Warning: Virtual environment not activated. Please activate it with 'source .venv/bin/activate'.")
    
    # Open browser
    webbrowser.open("http://localhost:5000")
    
    # Run Flask app
    app.run(debug=False, host="localhost", port=5000)