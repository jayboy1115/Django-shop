from flask import Flask
from waitress import serve
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Railway!"

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # Use waitress instead of app.run for production
    serve(app, host="0.0.0.0", port=port)