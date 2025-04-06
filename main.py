import os
import subprocess
from flask import Flask, render_template_string, request, redirect, url_for
from jinja2 import DictLoader

# Create Flask app and use "assets" as the static folder for background image.
app = Flask(__name__, static_folder="assets")

# Set up a DictLoader so that "base.html" is available to our templates.
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

# Directory where example files are stored
EXAMPLES_DIR = "examples"

# Utility function to list all _example.py files from the examples folder.
def get_example_files():
    files = []
    if os.path.isdir(EXAMPLES_DIR):
        for file in os.listdir(EXAMPLES_DIR):
            if file.endswith("_example.py"):
                files.append(file)
    return sorted(files)

# Route: Home page shows list of framework examples in a grid.
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

# Route: View the code of a selected example and show a form to run it.
@app.route("/view/<filename>", methods=["GET", "POST"])
def view_example(filename):
    filepath = os.path.join(EXAMPLES_DIR, filename)
    if not os.path.exists(filepath):
        return f"File {filename} not found.", 404

    # If POST, run the code and display the output.
    if request.method == "POST":
        try:
            result = subprocess.run(
                ["python", filepath],
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

    # Otherwise (GET): read the code from file and display it.
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

# Run the Flask app.
if __name__ == "__main__":
    # For demo purposes, use debug=True. Remove or adjust in production.
    app.run(debug=True)
