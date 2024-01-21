from flask import Flask, request, jsonify
from extractor import extract_data
from processor import process_data

def initialize_routes(app):

    @app.route('/extract', methods=['GET'])
    def extract():
        url = request.args.get('url')
        if not url:
            return jsonify({"error": "URL parameter is required"}), 400

        extracted_data = extract_data(url)
        if 'error' in extracted_data:
            return jsonify(extracted_data), 500

        processed_data = process_data(extracted_data)
        return jsonify(processed_data)
