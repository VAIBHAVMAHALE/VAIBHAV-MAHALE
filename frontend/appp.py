import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Vai Assistant!"

if __name__ == "__main__":
    # Get the port Render provides, default to 10000
    port = int(os.environ.get("PORT", 10000))
    # Bind to 0.0.0.0 so it’s accessible externally
    app.run(host="0.0.0.0", port=port)

