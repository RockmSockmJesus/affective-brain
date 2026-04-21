from typing import Dict
from .engine import VADVector

class MoodModulator:
    """
    Translates the VAD vector into complex, blended stylistic constraints.
    """
    def get_constraints(self, state: Dict) -> str:
        v, a, d = state['valence'], state['arousal'], state['dominance']
        
        constraints = []
        
        # 1. The Valence-Arousal Quadrants (The "Feel")
        if v < -0.3:
            if a > 0.3:
                constraints.append("Your tone is sharp, clipped, and visibly impatient.")
            elif a < -0.3:
                constraints.append("Your tone is heavy, slow, and tinged with melancholy.")
            else:
                constraints.append("Your tone is dissatisfied and cold.")
        elif v > 0.3:
            if a > 0.3:
                constraints.append("Your tone is energetic, warm, and enthusiastic.")
            elif a < -0.3:
                constraints.append("Your tone is serene, patient, and softly spoken.")
            else:
                constraints.append("Your tone is pleasantly agreeable.")
        else:
            constraints.append("Your tone is neutral and professional.")

        # 2. The Dominance Axis (The "Power")
        if d > 0.4:
            constraints.append("You speak with authority and confidence; do not hedge your statements.")
        elif d < -0.4:
            constraints.append("You are tentative and deferential; use hedging language (e.g., 'perhaps', 'I believe').")

        # 3. Energy Nuance (The "Presence")
        if a > 0.7:
            constraints.append("Use shorter sentences and high-intensity language.")
        elif a < -0.7:
            constraints.append("Your responses are minimalist and understated.")

        return " ".join(constraints)
