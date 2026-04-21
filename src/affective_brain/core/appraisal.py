from typing import Dict, List, Tuple
from .engine import VADVector

class AppraisalEngine:
    """
    The AppraisalEngine filters objective tone through the lens of the SOUL doc.
    It determines if a stimulus is 'positive' or 'negative' based on the agent's values.
    """
    def __init__(self, soul_config: Dict):
        self.soul = soul_config
        self.values = soul_config.get("core_values", "").lower()
        self.identity = soul_config.get("resting_mood", "").lower()

    def appraise(self, objective_stimulus: VADVector) -> VADVector:
        """
        Modifies the objective VAD vector based on cognitive appraisal.
        """
        v, a, d = objective_stimulus.valence, objective_stimulus.arousal, objective_stimulus.dominance
        
        # Example: If the agent values 'Intellectual Honesty', a 'Corrective' (negative valence)
        # stimulus might actually be appraised as Positive (Valence +) because it provides truth.
        if "honesty" in self.values or "logic" in self.values:
            # Detect 'Correction' pattern (Low valence, high dominance)
            if v < 0 and d > 0.3:
                v += 0.4  # Shift toward positive because the agent values the correction
                a += 0.2  # Increase arousal due to intellectual stimulation
        
        # Example: If the agent is 'Submissive' in its soul, a dominant stimulus 
        # might increase its own dominance (reactionary) or crash it further.
        if "servant" in self.identity or "humble" in self.identity:
            if d > 0.5:
                d -= 0.2 # Feel more submissive in the face of authority
                v -= 0.1 # Slight stress
        
        return VADVector(
            valence=max(-1.0, min(1.0, v)),
            arousal=max(-1.0, min(1.0, a)),
            dominance=max(-1.0, min(1.0, d))
        )
