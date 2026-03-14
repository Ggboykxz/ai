# --- NEXUS_AI_SYSTEM/07_INFERENCE_ENGINE/generation/text_generator.py ---

from typing import Dict, Any, Optional
import time

# Use a relative import to depend on the ModelLoader in a sibling directory.
# This will only work if the parent directory is a package (contains __init__.py)
# and the script is run as part of that package.
from ..core.model_loader import ModelLoader

class TextGenerator:
    """
    Orchestrates the text generation process using a loaded model and tokenizer.

    This class takes a user prompt, formats it, passes it to the model, and then
    decodes the output back into human-readable text.
    """

    def __init__(self, model: Any, tokenizer: Any):
        """
        Initializes the generator with a loaded model and tokenizer.

        Args:
            model (Any): The loaded AI model object.
            tokenizer (Any): The loaded tokenizer object.
        """
        if not model or not tokenizer:
            raise ValueError("Model and tokenizer must be provided.")
        self.model = model
        self.tokenizer = tokenizer

    def generate(self, prompt: str, generation_params: Optional[Dict] = None) -> str:
        """
        Generates text based on a given prompt and generation parameters.

        Args:
            prompt (str): The input text to the model.
            generation_params (Optional[Dict]): A dictionary of parameters controlling
                the generation process (e.g., max_length, temperature, top_p).

        Returns:
            str: The generated text, decoded from the model's output.
        """
        print("--- Generating text... ---")
        if generation_params is None:
            generation_params = self._get_default_params()

        print(f"Prompt: '{prompt[:100]}...'")
        print(f"Params: {generation_params}")

        # 1. Tokenize the input prompt
        input_tokens = self.tokenizer.encode(prompt)
        print(f"Input tokens (simulated): {input_tokens}")

        # 2. Pass tokens to the model to get output tokens
        start_time = time.time()
        time.sleep(1.5) # Simulate model thinking time
        num_new_tokens = generation_params.get('max_new_tokens', 50)
        output_tokens = input_tokens + [1] * num_new_tokens
        end_time = time.time()
        
        print(f"Output tokens (simulated): {output_tokens}")

        # 3. Decode the output tokens into a string
        generated_text = self.tokenizer.decode(output_tokens)

        duration = end_time - start_time
        print(f"Generation finished in {duration:.2f}s.")
        
        return generated_text

    def _get_default_params(self) -> Dict:
        """Returns a default set of generation parameters."""
        return {
            'max_new_tokens': 50,
            'temperature': 0.7,
            'top_p': 0.9,
            'do_sample': True
        }

if __name__ == '__main__':
    print("--- Running Text Generator Example ---")
    
    # This example demonstrates how to use the classes if they are correctly structured
    # in a Python package. Running this script directly will likely fail unless the
    # PYTHONPATH is configured to recognize the parent directories.
    
    print("Initializing ModelLoader...")
    # In a real application, you'd inject these dependencies.
    # For this example, we instantiate them directly.
    loader = ModelLoader("nexus-ai/model-v0.1-simulated")
    loader.load_model()
    model, tokenizer = loader.get_model_and_tokenizer()

    # Initialize the generator
    text_gen = TextGenerator(model=model, tokenizer=tokenizer)

    # Generate text
    my_prompt = "The purpose of a self-improving AI is"
    generated_output = text_gen.generate(prompt=my_prompt)

    print("\n--- Generated Output ---")
    print(generated_output)

