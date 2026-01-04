from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# Inject BACKEND_URL into all templates. Set via env var BACKEND_URL; fallback to http://127.0.0.1:8000
_BACKEND_URL = os.environ.get('BACKEND_URL', 'http://127.0.0.1:8000')

@app.context_processor
def inject_backend():
    return dict(backend_url=_BACKEND_URL)

@app.route('/')
def index():
    return render_template('openai_index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
