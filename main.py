import os
import subprocess
from flask import Flask, render_template_string, request, redirect, url_for
from jinja2 import DictLoader

# Create Flask app and use "assets" as the static folder for background image.
app = Flask(__name__, static_folder="assets")

# Base HTML template shared by all pages.
BASE_TEMPLATE = """
<!doctype html>
<html>
  <head>
    <title>Watsonx Client Demo</title>
    <style>
      body {
         background: url("{{ url_for('static', filename='background.jpg') }}") no-repeat center center fixed;
         background-size: cover;
         color: #ffffff;
         font-family: Arial, sans-serif;
         margin: 0;
         padding: 0;
      }
      .container {
         background: rgba(0, 0, 0, 0.7);
         margin: 50px auto;
         max-width: 800px;
         padding: 20px;
         border-radius: 10px;
      }
      a {
         color: #66ccff;
         text-decoration: none;
      }
      a:hover {
         text-decoration: underline;
      }
      pre {
         background-color: #333;
         padding: 10px;
         border-radius: 5px;
         overflow-x: auto;
      }
      .output {
         background-color: #222;
         padding: 10px;
         border-radius: 5px;
         margin-top: 20px;
         white-space: pre-wrap;
      }
      button {
         background-color: #66ccff;
         border: none;
         padding: 10px 20px;
         font-size: 16px;
         border-radius: 5px;
         cursor: pointer;
      }
      button:hover {
         background-color: #55bbdd;
      }
      /* Grid container for examples */
      .grid-container {
         display: grid;
         grid-template-columns: repeat(3, 1fr);
         gap: 20px;
         margin-top: 20px;
      }
      .grid-item {
         background-color: #444;
         padding: 20px;
         border-radius: 8px;
         text-align: center;
         font-size: 18px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      {% block content %}{% endblock %}
    </div>
  </body>
</html>
"""
app.jinja_loader = DictLoader({"base.html": BASE_TEMPLATE})

# Directory where example files are stored.
EXAMPLES_DIR = "examples"

def get_example_files():
    files = []
    if os.path.isdir(EXAMPLES_DIR):
        for file in os.listdir(EXAMPLES_DIR):
            if file.endswith("_example.py"):
                files.append(file)
    return sorted(files)

def select_venv(filename):
    """
    Choose the appropriate Python interpreter based on the example's filename.
    If the filename contains:
      - "beeai"         use .venv_beeai
      - "langflow"      use .venv_langflow
      - "watsonx_sdk"   use .venv_watsonx_sdk
      - "langraph"      use .venv_langraph
    Otherwise, default to the base environment (.venv).
    """
    framework_map = {
        "beeai": ".venv_beeai",
        "langflow": ".venv_langflow",
        "watsonx_sdk": ".venv_watsonx_sdk",
        "langraph": ".venv_langraph",
    }
    for key, venv in framework_map.items():
        if key in filename:
            return os.path.join(os.getcwd(), venv, "bin", "python")
    # Default to base environment if no framework-specific keyword is found.
    return os.path.join(os.getcwd(), ".venv", "bin", "python")

@app.route("/")
def index():
    files = get_example_files()
    index_template = """
    {% extends "base.html" %}
    {% block content %}
      <h1>Watsonx Client Demo: Framework Examples</h1>
      <div class="grid-container">
        {% for file in files %}
          <div class="grid-item">
            <a href="{{ url_for('view_example', filename=file) }}">
              {{ file.replace('_example.py','').replace('_', ' ') | title }}
            </a>
          </div>
        {% endfor %}
      </div>
    {% endblock %}
    """
    return render_template_string(index_template, files=files)

@app.route("/view/<filename>", methods=["GET", "POST"])
def view_example(filename):
    filepath = os.path.join(EXAMPLES_DIR, filename)
    if not os.path.exists(filepath):
        return f"File {filename} not found.", 404

    if request.method == "POST":
        try:
            python_executable = select_venv(filename)
            result = subprocess.run(
                [python_executable, filepath],
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            output = f"Error running the example: {e}"
        run_template = """
        {% extends "base.html" %}
        {% block content %}
          <h2>{{ filename.replace('_example.py','').replace('_', ' ') | title }} - Output</h2>
          <div class="output">{{ output }}</div>
          <br>
          <a href="{{ url_for('index') }}">Back to examples</a>
        {% endblock %}
        """
        return render_template_string(run_template, filename=filename, output=output)

    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    view_template = """
    {% extends "base.html" %}
    {% block content %}
      <h2>{{ filename.replace('_example.py','').replace('_', ' ') | title }} - Code</h2>
      <pre>{{ code }}</pre>
      <form method="post">
         <button type="submit">Run Example</button>
      </form>
      <br>
      <a href="{{ url_for('index') }}">Back to examples</a>
    {% endblock %}
    """
    return render_template_string(view_template, filename=filename, code=code)

if __name__ == "__main__":
    app.run(debug=True)
