# --- NEXUS_AI_SYSTEM/08_API_PLATFORM/api/api_server.py ---

from flask import Flask, request, jsonify
from typing import Optional, Dict

# Corrected import to use a relative path to the inference engine module.
# This makes the API platform a self-contained package.
from ..inference_engine import InferenceEngine

app = Flask(__name__)

# Global variable to hold the inference engine.
inference_engine: Optional[InferenceEngine] = None

def initialize_engine():
    """Loads the inference engine into the global scope."""
    global inference_engine
    if inference_engine is None:
        print("--- Initializing Inference Engine for the first time... ---")
        model_id = "nexus-ai/api-model-v0.1-simulated"
        inference_engine = InferenceEngine(model_path=model_id)
        print("--- Inference Engine ready. ---")

@app.route('/health', methods=['GET'])
def health_check():
    """A simple health check endpoint to confirm the server is running."""
    return jsonify({"status": "ok"}), 200

@app.route('/generate', methods=['POST'])
def generate_text():
    """
    The main endpoint for text generation.
    Accepts a JSON payload with a 'prompt' and optional 'generation_params'.
    """
    if not request.json or 'prompt' not in request.json:
        return jsonify({"error": "Invalid request. 'prompt' field is required."}), 400

    prompt = request.json['prompt']
    generation_params = request.json.get('generation_params') # Optional

    print(f"\n--- Received request for /generate ---")
    print(f"Prompt: {prompt[:100]}...")

    # Lazy initialization of the engine on the first request.
    initialize_engine()

    try:
        generated_text = inference_engine.run(prompt, generation_params)
        response_data = {
            'prompt': prompt,
            'generated_text': generated_text
        }
        return jsonify(response_data), 200
    except Exception as e:
        print(f"An error occurred during inference: {e}")
        return jsonify({"error": "Failed to generate text."}), 500

def run_server(host='0.0.0.0', port=5000):
    """Starts the Flask development server."""
    print(f"--- Starting API server on {host}:{port}... ---")
    app.run(host=host, port=port)

if __name__ == '__main__':
    # To run this server: 
    # 1. Make sure you have created __init__.py files in all relevant directories.
    # 2. Set the PYTHONPATH to the root of the project.
    # 3. Run: `python -m NEXUS_AI_SYSTEM.08_API_PLATFORM.api.api_server`
    run_server()

