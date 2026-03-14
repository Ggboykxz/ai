
from flask import Flask, request, jsonify

class APIServer:
    def __init__(self, api_platform):
        self.api_platform = api_platform
        self.logger = self.api_platform.logger
        self.ai_system = self.api_platform.ai_system
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/api/v1/inference", methods=["POST"])
        def inference():
            data = request.get_json()
            input_text = data.get("input_text")
            if not input_text:
                return jsonify({"error": "Missing input_text"}), 400

            # Run inference
            output = self.ai_system.inference_engine.run_inference(input_text)
            return jsonify({"output_text": output})

    def start(self):
        self.logger.log("Starting API server...")
        # Note: In a production environment, use a proper WSGI server like Gunicorn
        self.app.run(host="0.0.0.0", port=5000)
