def initialize_routes(app):
    @app.route('/')
    def index():
        return "Welcome to the News Article Extractor API!"
