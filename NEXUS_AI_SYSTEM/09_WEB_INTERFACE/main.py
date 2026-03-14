
import streamlit as st
from NEXUS_AI_SYSTEM.src.nexus_ai_system.ai_system.main import AISystem

class WebInterface:
    def __init__(self, ai_system: AISystem):
        self.ai_system = ai_system

    def run(self):
        st.title("Nexus AI System")

        # Add a text input for user queries
        user_query = st.text_input("Ask me anything:")

        if st.button("Submit"):
            if user_query:
                # Run inference
                output = self.ai_system.inference_engine.run_inference(user_query)
                st.write("**Answer:**")
                st.write(output)
            else:
                st.write("Please enter a query.")

if __name__ == "__main__":
    # This assumes the AI system is initialized and passed to the web interface
    # In a real application, this would be handled by a main script
    # ai_system = AISystem()
    # ai_system.initialize()
    # web_interface = WebInterface(ai_system)
    # web_interface.run()
    pass
