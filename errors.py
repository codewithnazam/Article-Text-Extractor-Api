from flask import jsonify
from werkzeug.exceptions import HTTPException

def handle_errors(app):
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Generic error handler for HTTP exceptions."""
        response = e.get_response()
        response.data = jsonify({"error": e.description})
        response.content_type = "application/json"
        return response

    # This can be expanded with more specific error handlers if needed
