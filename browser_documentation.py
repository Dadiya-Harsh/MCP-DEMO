import os
import sys
import subprocess
import webbrowser
from pathlib import Path
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from dotenv import load_dotenv, set_key
import markdown
import signal

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for flash messages

# Define base directory
BASE_DIR = Path(__file__).parent
LEARNING_DIR = BASE_DIR / "learning"
ENV_FILE = BASE_DIR / ".env"

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

# Define supported environment variables
ENV_VARIABLES = [
    "GROQ_API_KEY",
    "GEMINI_API_KEY",
    "TAVILY_API_KEY",
    "DATABASE_URL",
    "TRANSPORT",
    "model_llm",
    "DATABASE_URI",
    "ALLOWED_BASE_PATH",
]

# Global variable to track running process
current_process = None

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
    global current_process
    module_name = request.form.get("module_name")
    script_name = request.form.get("script_name")

    if module_name not in MODULES:
        return jsonify({"error": f"Module '{module_name}' not found."}), 400

    module_info = MODULES[module_name]
    script_path = module_info["path"] / script_name

    if not script_path.exists() or not script_path.is_file():
        return jsonify({"error": f"Script '{script_name}' not found."}), 400

    try:
        # If a process is already running, terminate it
        if current_process is not None:
            current_process.terminate()
            current_process.wait(timeout=5)
            current_process = None

        # Start the script as a subprocess
        current_process = subprocess.Popen(
            [sys.executable, str(script_path)],
            cwd=module_info["path"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        # Read output and error streams
        stdout, stderr = current_process.communicate(timeout=30)
        current_process = None  # Reset process after completion
        return jsonify({"output": stdout, "error": stderr})
    except subprocess.TimeoutExpired:
        if current_process:
            current_process.terminate()
            current_process = None
        return jsonify({"error": "Script execution timed out."}), 500
    except Exception as e:
        if current_process:
            current_process.terminate()
            current_process = None
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route("/stop_script", methods=["POST"])
def stop_script():
    """Stop the currently running script."""
    global current_process
    if current_process is not None:
        try:
            current_process.terminate()
            current_process.send_signal(signal.SIGTERM)
            current_process.wait(timeout=5)
            current_process = None
            return jsonify({"message": "Script stopped successfully."})
        except Exception as e:
            current_process = None
            return jsonify({"error": f"Error stopping script: {str(e)}"}), 500
    return jsonify({"message": "No script is currently running."})

@app.route("/env", methods=["GET", "POST"])
def env():
    """Render and handle the environment variables form."""
    if request.method == "POST":
        try:
            for var in ENV_VARIABLES:
                value = request.form.get(var, "").strip()
                set_key(ENV_FILE, var, value)
            flash("Environment variables updated successfully!", "success")
            # Reload environment variables
            load_dotenv(override=True)
        except Exception as e:
            flash(f"Error updating environment variables: {str(e)}", "error")
        return redirect(url_for("env"))

    # Load current values from .env, flag if set
    env_values = {var: os.getenv(var, "") for var in ENV_VARIABLES}
    env_set = {var: bool(os.getenv(var)) for var in ENV_VARIABLES}
    return render_template(
        "env.html",
        modules=MODULES,
        env_variables=ENV_VARIABLES,
        env_values=env_values,
        env_set=env_set
    )

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