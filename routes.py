from flask import Flask, request, jsonify
from flask_limiter import Limiter
from extractor import extract_data
from processor import process_data
from werkzeug.exceptions import HTTPException, BadRequest

app = Flask(__name__)



def initialize_routes(app, limiter):
    @app.route('/extract', methods=['GET'])
    @limiter.limit("2 per minute", error_message='You have exceeded the rate limit of 2 requests per minute. Please wait a moment and try again.')  # Apply rate limiting: 2 requests per minute
    def extract():
        url = request.args.get('url')
        if not url:
            return jsonify({"error": "URL parameter is required"}), 400

        try:
            extracted_data = extract_data(url)
            if 'error' in extracted_data:
                raise BadRequest(extracted_data['error'])
            processed_data = process_data(extracted_data)
            return jsonify(processed_data)
        except BadRequest as e:
            return jsonify({"error": str(e.description)}), e.code
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred"}), 500

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy'}), 200
