# =============================================================
# app.py  - Flask UI
# Run:  flask --app app run --host 0.0.0.0 --port 5000
# =============================================================

import os
from flask import Flask, render_template

app = Flask(__name__)

# API URL
API_BASE = os.environ.get("API_BASE", "http://127.0.0.1:8000")


@app.context_processor
def inject_api_base():
    return {"api_base": API_BASE}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test")
def test_page():
    return render_template("test.html")


@app.route("/terminal")
def terminal_page():
    return render_template("terminal.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
