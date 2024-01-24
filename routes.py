from flask import Flask, request, jsonify
from extractor import extract_data
from processor import process_data

def initialize_routes(app):

    @app.route('/extract', methods=['GET'])
    def extract():
        url = request.args.get('url')
        if not url:
            return jsonify({"error": "URL parameter is required"}), 400

        try:
            extracted_data = extract_data(url)
            processed_data = process_data(extracted_data)
            return jsonify(processed_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy'}), 200
