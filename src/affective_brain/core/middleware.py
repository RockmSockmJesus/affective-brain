import time
from typing import Dict, Any
from .engine import VADVector

class AffectiveMiddleware:
    """
    Middleware that wraps a standard LLM call.
    It handles the emotional state update and injects the 
    resultant constraints into the system prompt.
    """
    def __init__(self, brain_instance):
        self.brain = brain_instance

    def wrap_request(self, user_input: str, system_prompt: str) -> str:
        \"\"\"
        Processes the input through the brain and returns an augmented 
        system prompt containing the emotional constraints.
        \"\"\"
        # 1. Update emotional state based on input
        result = self.brain.process_input(user_input)
        constraints = result['constraints']
        
        # 2. Inject constraints into the system prompt
        augmented_prompt = (
            f"{system_prompt}\n\n"
            f"--- CURRENT EMOTIONAL STATE ---\n"
            f"{constraints}\n"
            f"Maintain this emotional tone consistently in your response."
        )
        
        return augmented_prompt

    def wrap_response(self, llm_response: str):
        \"\"\"
        Optionally, the agent's own response can affect its mood 
        (e.g., expressing anger might increase arousal).
        \"\"\"
        # We treat the agent's own output as a stimulus to maintain continuity
        # (The agent 'feels' its own expressed emotion)
        self.brain.process_input(llm_response)
