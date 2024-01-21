from flask import Flask
from routes import initialize_routes
from errors import handle_errors

app = Flask(__name__)

# Initialize routes
initialize_routes(app)
# Initialize errors
handle_errors(app)

if __name__ == "__main__":
    app.run(debug=True)
