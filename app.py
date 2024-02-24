from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import nltk
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from routes import initialize_routes
from errors import handle_errors

# Load environment variables
load_dotenv()

nltk.download('punkt')

app = Flask(__name__)
CORS(app, resources={r"/extract": {"origins": os.getenv("CORS_ORIGIN")}})

# Initialize Limiter
limiter = Limiter(app=app, key_func=get_remote_address)

initialize_routes(app, limiter)
handle_errors(app)

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "False") == "True")
