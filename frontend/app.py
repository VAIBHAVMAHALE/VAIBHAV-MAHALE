from flask import Flask, render_template
import os

# Create Flask app
app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

# Backend URL (set in Render Environment Variables)
# Fallback works for local development
BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")


# Make backend_url available in all templates
@app.context_processor
def inject_backend_url():
    return {"backend_url": BACKEND_URL}


# Routes
@app.route("/")
def index():
    return render_template("openai_index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/tasks")
def tasks():
    return render_template("tasks.html")


# Run app (IMPORTANT FOR RENDER)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
