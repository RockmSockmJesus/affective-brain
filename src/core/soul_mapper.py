import json
import os
from typing import Dict, Optional
from .engine import VADVector

class SoulMapper:
    """
    Maps the natural language descriptions in a SOUL doc 
    to the mathematical constants of the AffectiveCore.
    """
    
    # Mapping natural language keywords to VAD offsets
    MOOD_MAP = {
        "stoic": {"v": 0.0, "a": -0.3, "d": 0.2},
        "melancholic": {"v": -0.3, "a": -0.2, "d": -0.1},
        "cheerful": {"v": 0.5, "a": 0.3, "d": 0.0},
        "anxious": {"v": -0.2, "a": 0.6, "d": -0.4},
        "aggressive": {"v": -0.4, "a": 0.7, "d": 0.6},
        "serene": {"v": 0.3, "a": -0.5, "d": 0.2},
    }

    STABILITY_MAP = {
        "fast": 0.15,    # High decay = quick return to baseline
        "resilient": 0.10,
        "slow": 0.02,    # Low decay = emotions linger
        "lingering": 0.01,
        "volatile": 0.05, # Medium decay but likely high sensitivity
    }

    SENSITIVITY_MAP = {
        "high": 0.6,     # Reacts strongly to every stimulus
        "medium": 0.3,
        "low": 0.1,      # Almost unfazed
        "thick-skinned": 0.05,
    }

    @classmethod
    def map_soul_to_params(cls, soul_data: Dict) -> Dict:
        """
        Takes synthesized answers and returns AffectiveCore parameters.
        """
        # 1. Calculate Baseline VAD
        resting_mood = soul_data.get("resting_mood", "").lower()
        baseline_v = 0.0
        baseline_a = 0.0
        baseline_d = 0.0

        for key, val in cls.MOOD_MAP.items():
            if key in resting_mood:
                baseline_v = val["v"]
                baseline_a = val["a"]
                baseline_d = val["d"]
                break
        
        # Power dynamic adjustment for dominance
        power = soul_data.get("power_dynamic", "").lower()
        if "servant" in power or "humble" in power:
            baseline_d -= 0.3
        elif "mentor" in power or "authority" in power:
            baseline_d += 0.3

        # 2. Calculate Decay Rate
        stability = soul_data.get("emotional_stability", "").lower()
        decay = 0.05 # default
        for key, val in cls.STABILITY_MAP.items():
            if key in stability:
                decay = val
                break
        
        # 3. Calculate Sensitivity
        sensitivity = soul_data.get("sensitivity", "").lower()
        sens = 0.3 # default
        for key, val in cls.SENSITIVITY_MAP.items():
            if key in sensitivity:
                sens = val
                break

        return {
            "baseline": VADVector(baseline_v, baseline_a, baseline_d),
            "decay_rate": decay,
            "sensitivity": sens
        }
