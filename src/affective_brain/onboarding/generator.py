import random
from typing import Dict
from .engine import VADVector

class PersonalityGenerator:
    """
    Generates a randomized personality based on a Gaussian distribution
    to simulate the natural spectrum of human temperaments.
    """
    
    # Gaussian Parameters: (mean, standard_deviation)
    # Most people cluster around 0, but outliers exist.
    SPECTRUM = {
        "valence": (0.0, 0.3),    # Most are neutral/slightly positive
        "arousal": (0.0, 0.4),    # Wide range of energy levels
        "dominance": (0.0, 0.3),  # Most are balanced, few are extremely dominant/submissive
        "decay_rate": (0.05, 0.03),
        "sensitivity": (0.3, 0.1)
    }

    @classmethod
    def generate_random_soul(cls) -> Dict:
        """
        Samples from the bell curve to create a unique, coherent personality.
        """
        # Generate raw Gaussian values
        raw_v = random.gauss(*cls.SPECTRUM["valence"])
        raw_a = random.gauss(*cls.SPECTRUM["arousal"])
        raw_d = random.gauss(*cls.SPECTRUM["dominance"])
        
        # Clamp to [-1, 1]
        v = max(-1.0, min(1.0, raw_v))
        a = max(-1.0, min(1.0, raw_a))
        d = max(-1.0, min(1.0, raw_d))
        
        # Generate a human-readable label based on the resulting VAD
        label = cls._map_vad_to_label(v, a, d)
        
        return {
            "resting_mood": label,
            "emotional_stability": "Randomized" if random.random() > 0.5 else "Stable",
            "sensitivity": "Randomized",
            "power_dynamic": "Randomized",
            "core_values": "Randomly assigned biological drive",
            "raw_vad": {"valence": v, "arousal": a, "dominance": d}
        }

    @staticmethod
    def _map_vad_to_label(v, a, d) -> str:
        """Basic mapping to give the randomized soul a readable identity."""
        if v > 0.4 and a > 0.4: return "Exuberant"
        if v < -0.4 and a > 0.4: return "Irritable"
        if v < -0.4 and a < -0.2: return "Melancholic"
        if v > 0.4 and a < -0.2: return "Serene"
        if d > 0.6: return "Commanding"
        if d < -0.6: return "Timid"
        return "Balanced"
