import json
import os
from typing import Optional

class PersistenceLayer:
    """
    Handles saving and loading the brain's current emotional state 
    and the SOUL configuration.
    """
    def __init__(self, storage_dir: str = "data"):
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)
        
        self.state_file = os.path.join(storage_dir, "current_state.json")
        self.soul_file = os.path.join(storage_dir, "soul.json")

    def save_state(self, state: dict):
        """Saves the current VAD vector and timestamp."""
        with open(self.state_file, 'w') as f:
            json.dump(state, f)

    def load_state(self) -> Optional[dict]:
        """Loads the last saved state."""
        if not os.path.exists(self.state_file):
            return None
        with open(self.state_file, 'r') as f:
            return json.load(f)

    def save_soul(self, soul_data: dict):
        """Saves the parsed soul parameters."""
        with open(self.soul_file, 'w') as f:
            json.dump(soul_data, f)

    def load_soul(self) -> Optional[dict]:
        """Loads the soul parameters."""
        if not os.path.exists(self.soul_file):
            return None
        with open(self.soul_file, 'r') as f:
            return json.load(f)
