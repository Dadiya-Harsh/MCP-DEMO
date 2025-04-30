import os
import subprocess
import sys
from pathlib import Path
import markdown
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define base directory
BASE_DIR = Path(__file__).parent
LEARNING_DIR = BASE_DIR / "learning"

# Define modules and their descriptions
MODULES = {
    "simple": {"path": LEARNING_DIR / "simple", "desc": "Basic MCP examples (stdio and SSE)"},
    "groq": {"path": LEARNING_DIR / "groq", "desc": "Groq LLM integration"},
    "Servers": {"path": LEARNING_DIR / "Servers", "desc": "Various server implementations"},
    "Clients": {"path": LEARNING_DIR / "Clients", "desc": "Advanced client implementations"},
    "asyncoronus python": {
        "path": LEARNING_DIR / "asyncoronus python",
        "desc": "Async programming examples",
    },+
}

def display_welcome():
    """Display a welcome message and project overview."""
    print("\n=== Welcome to MCP-DEMO: My Learning Journey with Model Context Protocol ===\n")
    readme_path = BASE_DIR / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
            print(content[:200] + "..." if len(content) > 200 else content)
            print("\nRead the full README.md in the root directory for more details.")
    else:
        print("README.md not found. This repo documents my MCP learning journey.")

def list_modules():
    """List available modules."""
    print("\nAvailable Learning Modules:")
    for i, (name, info) in enumerate(MODULES.items(), 1):
        print(f"{i}. {name}: {info['desc']}")

def display_module_docs(module_name):
    """Display the complete README.md for a specific module."""
    module_info = MODULES.get(module_name)
    if not module_info:
        print(f"Error: Module '{module_name}' not found.")
        return
    readme_path = module_info["path"] / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
            print(f"\n=== Documentation for {module_name} ===\n")
            print(content)  # Print the full content without truncation
    else:
        print(f"No README.md found in {module_name} directory.")

def list_scripts(module_name):
    """List executable Python scripts in a module directory."""
    module_info = MODULES.get(module_name)
    if not module_info:
        print(f"Error: Module '{module_name}' not found.")
        return []
    scripts = [f.name for f in module_info["path"].glob("*.py") if f.is_file()]
    if not scripts:
        print(f"No Python scripts found in {module_name} directory.")
    else:
        print(f"\nPython scripts in {module_name}:")
        for i, script in enumerate(scripts, 1):
            print(f"{i}. {script}")
    return scripts

def run_script(module_name, script_name):
    """Run a Python script in the specified module directory."""
    module_info = MODULES.get(module_name)
    if not module_info:
        print(f"Error: Module '{module_name}' not found.")
        return
    script_path = module_info["path"] / script_name
    if not script_path.exists() or not script_path.is_file():
        print(f"Error: Script '{script_name}' not found in {module_name} directory.")
        return
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=module_info["path"],
            check=True,
            text=True,
            capture_output=True,
        )
        print(f"\nOutput of {script_name}:\n{result.stdout}")
        if result.stderr:
            print(f"Errors (if any):\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        print(f"Error output:\n{e.stderr}")
    except Exception as e:
        print(f"Unexpected error running {script_name}: {e}")

def main():
    """Main interactive loop."""
    session = PromptSession("Select an option (1-4): ", multiline=False)
    bindings = KeyBindings()

    while True:
        display_welcome()
        list_modules()
        print("\nOptions:")
        print("1. View module documentation")
        print("2. List scripts in a module")
        print("3. Run a script")
        print("4. Exit")
        
        choice = session.prompt()
        
        if choice == "1":
            module_name = input("\nEnter module name (e.g., simple, groq, Servers): ").strip()
            display_module_docs(module_name)
        elif choice == "2":
            module_name = input("\nEnter module name (e.g., simple, groq, Servers): ").strip()
            list_scripts(module_name)
        elif choice == "3":
            module_name = input("\nEnter module name (e.g., simple, groq, Servers): ").strip()
            scripts = list_scripts(module_name)
            if scripts:
                script_idx = input("Enter script number to run (e.g., 1): ").strip()
                try:
                    script_idx = int(script_idx) - 1
                    if 0 <= script_idx < len(scripts):
                        run_script(module_name, scripts[script_idx])
                    else:
                        print("Invalid script number.")
                except ValueError:
                    print("Please enter a valid number.")
        elif choice == "4":
            print("Exiting MCP-DEMO. Happy learning!")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    if not os.getenv("VIRTUAL_ENV"):
        print("Warning: Virtual environment not activated. Please activate it with 'source .venv/bin/activate'.")
    try:
        import prompt_toolkit
        import markdown
        import dotenv
    except ImportError:
        print("Error: Required dependencies missing. Please run 'uv pip install -r requirements.txt'.")
        sys.exit(1)
    
    main()