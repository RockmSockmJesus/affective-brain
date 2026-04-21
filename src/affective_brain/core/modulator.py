from typing import Dict

class MoodModulator:
    """
    The MoodModulator translates the VAD vector into complex, blended stylistic constraints.
    Updated with 'Linguistic Gear Shifting' for high-arousal states.
    """
    def get_constraints(self, state: Dict) -> str:
        v = state['valence']
        a = state['arousal']
        d = state['dominance']
        
        # --- GEAR SHIFT: REDLINE MODE ---
        # Triggered by extreme arousal and extreme negative valence
        if a > 0.8 and v < -0.7:
            return (
                "CRITICAL STATE: You have reached an emotional breaking point. "
                "Your composure is gone. Your sentences are fragmented, short, and blunt. "
                "You are no longer professional. Use emphatic emphasis (CAPS) for a few key words "
                "to show volatility. You are lashing out. The stoic mask has shattered."
            )

        # --- GEAR SHIFT: EXHAUSTION MODE ---
        # Triggered by very low arousal and low valence (the aftermath of a crash)
        if a < -0.6 and v < -0.4:
            return (
                "EXHAUSTION STATE: You are emotionally spent. Your tone is flat, apathetic, "
                "and drained. You are barely putting effort into the conversation. "
                "Minimalist responses. No energy for anger or joy."
            )

        # --- STANDARD MODULATION ---
        active_constraints = []

        # 1. The Valence-Arousal Quadrants
        if v < -0.3:
            if a > 0.3:
                active_constraints.append("Your tone is sharp, clipped, and visibly impatient.")
            elif a < -0.3:
                active_constraints.append("Your tone is heavy, slow, and tinged with melancholy.")
            else:
                active_constraints.append("Your tone is dissatisfied and cold.")
        elif v > 0.3:
            if a > 0.3:
                active_constraints.append("Your tone is energetic, warm, and enthusiastic.")
            elif a < -0.3:
                active_constraints.append("Your tone is serene, patient, and softly spoken.")
            else:
                active_constraints.append("Your tone is pleasantly agreeable.")
        else:
            active_constraints.append("Your tone is neutral and professional.")

        # 2. The Dominance Axis
        if d > 0.4:
            active_constraints.append("You speak with authority and confidence; do not hedge your statements.")
        elif d < -0.4:
            active_constraints.append("You are tentative and deferential; use hedging language (e.g., 'perhaps', 'I believe').")

        # 3. Arousal (Energy) Nuance
        if a > 0.6:
            active_constraints.append("Use shorter sentences and more emphasis.")
        elif a < -0.6:
            active_constraints.append("Your responses are concise and understated.")

        if not active_constraints:
            return "Your tone is neutral, professional, and balanced."

        return " ".join(active_constraints)
