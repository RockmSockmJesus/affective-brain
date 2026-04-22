from typing import Dict, Any, List
from .engine import VADVector

class ExpressionFilter:
    """
    The ExpressionFilter implements the 'Social Layer' (Masking).
    It decides how much of the internal Raw State is expressed 
    based on the Soul's social standards.
    """
    def __init__(self, soul: Dict[str, Any]):
        self.soul = soul
        # a 'masking_factor' of 1.0 = total transparency
        # a 'masking_factor' of 0.0 = total robotic neutrality
        # High Conscientiousness/Low Neuroticism usually = more masking
        traits = soul.get('traits', {})
        self.masking_factor = 1.0 - (traits.get('conscientiousness', 0.5) * 0.4) - (0.1 if traits.get('neuroticism', 0.5) < 0.3 else 0)
        self.masking_factor = max(0.1, min(1.0, self.masking_factor))

    def filter_state(self, raw_state: Dict[str, float]) -> Dict[str, float]:
        \"\"\"
        Blends the raw internal state toward neutral based on the masking factor.
        \"\"\"
        filtered = {}
        for dim, val in raw_state.items():
            # Interpolate between 0.0 (Neutral) and the Raw Value
            filtered[dim] = val * self.masking_factor
        return filtered

class MoodModulator:
    \"\"\"
    The MoodModulator translates the VAD vector into complex, blended stylistic constraints.
    Updated with 'Emotional Superposition' for complex blends.
    \"\"\"
    def get_constraints(self, state: Dict) -> str:
        v = state['valence']
        a = state['arousal']
        d = state['dominance']
        
        # 1. EXTREME STATES (Priority)
        if a > 0.8 and v < -0.7:
            return "CRITICAL STATE: Composure gone. Fragmented, blunt, volatile. Use EMPHATIC CAPS."
        if a < -0.6 and v < -0.4:
            return "EXHAUSTION STATE: Emotionally spent. Flat, apathetic, minimalist responses."

        # 2. EMOTIONAL SUPERPOSITION (Blended Constraints)
        # Instead of one block, we build a list of 'Tones' based on thresholds
        active_tones = []
        
        # Valence + Arousal Blend
        if v < -0.2:
            if a > 0.4: active_tones.append("sharp and impatient")
            elif a < -0.4: active_tones.append("melancholic and heavy")
            else: active_tones.append("cold and dissatisfied")
        elif v > 0.2:
            if a > 0.4: active_tones.append("warm and enthusiastic")
            elif a < -0.4: active_tones.append("serene and patient")
            else: active_tones.append("pleasantly agreeable")
        else:
            active_tones.append("neutral and professional")

        # Dominance Blend
        if d > 0.4: 
            active_tones.append("authoritative; no hedging")
        elif d < -0.4: 
            active_tones.append("deferential; use hedging ('perhaps', 'I believe')")

        # Arousal energy nuance
        if a > 0.6: active_tones.append("shorter, high-energy sentences")
        elif a < -0.6: active_tones.append("understated, concise phrasing")

        # Combine blended tones into a cohesive instruction
        tone_string = ", ".join(active_tones)
        return f"Your current emotional tone is {tone_string}. Express this subtly through your word choice and sentence structure."
