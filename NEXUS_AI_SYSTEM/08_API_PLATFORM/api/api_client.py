# --- NEXUS_AI_SYSTEM/08_API_PLATFORM/api/api_client.py ---

import requests
import json
from typing import Dict, Optional

class APIClient:
    """
    A client for interacting with the NEXUS-AI API server.
    
    This class provides a simple, high-level interface to make requests
    to the `/generate` endpoint.
    """

    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        """
        Initializes the client with the server's base URL.

        Args:
            base_url (str): The base URL of the API server.
        """
        self.base_url = base_url
        self.generate_url = f"{self.base_url}/generate"
        self.health_url = f"{self.base_url}/health"

    def is_server_ready(self) -> bool:
        """
        Checks if the server is running and healthy.

        Returns:
            bool: True if the server responds with a 200 status, False otherwise.
        """
        try:
            response = requests.get(self.health_url, timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def generate(self, prompt: str, generation_params: Optional[Dict] = None) -> Dict:
        """
        Sends a request to the /generate endpoint.

        Args:
            prompt (str): The prompt to send to the model.
            generation_params (Optional[Dict]): A dictionary of generation parameters.

        Returns:
            Dict: The JSON response from the server. If an error occurs, a dictionary
                  containing an 'error' key is returned.
        """
        payload = {
            'prompt': prompt,
            'generation_params': generation_params
        }
        
        try:
            response = requests.post(self.generate_url, json=payload, timeout=60)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()
        except requests.exceptions.HTTPError as e:
            return {"error": f"HTTP Error: {e.response.status_code}", "details": e.response.text}
        except requests.exceptions.RequestException as e:
            # Handles connection errors, timeouts, etc.
            return {"error": f"Request failed: {e}"}

if __name__ == '__main__':
    print("--- Running API Client Example ---")
    
    client = APIClient()

    # 1. Check if the server is running before making a request.
    print(f"Checking server readiness at {client.base_url}...")
    if not client.is_server_ready():
        print("\nError: The API server is not running or is unreachable.")
        print("Please start the server first by running: `python api_server.py`")
    else:
        print("Server is ready.")
        
        # 2. Define a prompt and make a request.
        my_prompt = "What is the role of a Platform API in a modern AI system?"
        print(f"\nSending prompt: '{my_prompt}'")

        response = client.generate(my_prompt)

        # 3. Print the server's response.
        print("\n--- Server Response ---")
        if 'error' in response:
            print(f"An error occurred: {response['error']}")
            if 'details' in response:
                print(f"Details: {response['details']}")
        else:
            print(json.dumps(response, indent=2))

