from flask import Flask
from flask_cors import CORS
from routes import initialize_routes
from errors import handle_errors

import nltk  # Import NLTK here
nltk.download('punkt')  # Download the 'punkt' resource

app = Flask(__name__)
CORS(app, resources={r"/extract": {"origins": "https://codewithnazam.com"}})

# Initialize routes
initialize_routes(app)
# Initialize errors
handle_errors(app)

if __name__ == "__main__":
    app.run(debug=True)

