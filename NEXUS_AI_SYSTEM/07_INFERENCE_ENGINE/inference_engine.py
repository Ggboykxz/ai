# --- NEXUS_AI_SYSTEM/07_INFERENCE_ENGINE/inference_engine.py ---

from typing import Dict, Any, Optional

# Correctly import the necessary components using relative paths
from .core.model_loader import ModelLoader
from .generation.text_generator import TextGenerator

class InferenceEngine:
    """
    The main entry point for running text generation.

    This class encapsulates the entire inference pipeline, from loading the model
    to generating a response from a prompt.
    """

    def __init__(self, model_path: str, model_config: Optional[Dict] = None):
        """
        Initializes the entire inference engine.

        Args:
            model_path (str): The path or identifier of the model to be loaded.
            model_config (Optional[Dict]): Configuration for the model loader.
        """
        print(f"--- Initializing Inference Engine for model: {model_path} ---")
        self.model_path = model_path
        self.model_config = model_config
        
        # 1. Load the model
        self.loader = ModelLoader(self.model_path, self.model_config)
        self.loader.load_model()
        model, tokenizer = self.loader.get_model_and_tokenizer()
        
        # 2. Initialize the generator with the loaded model and tokenizer
        self.generator = TextGenerator(model, tokenizer)
        
        print("--- Inference Engine successfully initialized. ---")

    def run(self, prompt: str, generation_params: Optional[Dict] = None) -> str:
        """
        Runs the full generation pipeline from prompt to output text.

        Args:
            prompt (str): The input text to the model.
            generation_params (Optional[Dict]): Parameters for text generation.

        Returns:
            str: The generated text.
        """
        print(f"\n--- Running inference for prompt: '{prompt[:100]}...' ---")
        
        # Use the generator to produce the output
        generated_text = self.generator.generate(prompt, generation_params)
        
        return generated_text

if __name__ == '__main__':
    print("--- Running Inference Engine Example ---")

    # This assumes the script is run as part of a package.
    # E.g., `python -m NEXUS_AI_SYSTEM.07_INFERENCE_ENGINE.inference_engine`
    
    model_id = "nexus-ai/generation-0-simulated"

    # 1. Create an instance of the engine
    # This will automatically load the (simulated) model
    engine = InferenceEngine(model_path=model_id)

    # 2. Define a prompt and run inference
    user_prompt = "Explain the concept of emergent abilities in large language models."
    
    # Optional: Define generation parameters
    params = {
        'max_new_tokens': 75,
        'temperature': 0.8
    }

    # 3. Get the result
    output = engine.run(user_prompt, generation_params=params)

    print("\n--- Final Output from Engine ---")
    print(output)

