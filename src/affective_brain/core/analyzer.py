import random
from typing import Dict, Tuple
from .engine import VADVector

class ToneAnalyzer:
    """
    The ToneAnalyzer is responsible for mapping raw text to VAD coordinates.
    In a production environment, this would call a specialized model or a 
    fine-tuned LLM. For the core implementation, we provide a structured 
    prompt-based analyzer and a heuristic fallback.
    """

    def __init__(self, model_client=None):
        self.model_client = model_client

    def analyze(self, text: str) -> VADVector:
        """
        Analyze text and return a VADVector.
        """
        if self.model_client:
            return self._analyze_with_llm(text)
        return self._heuristic_analyze(text)

    def _analyze_with_llm(self, text: str) -> VADVector:
        """
        Constructs a system prompt to force the LLM to act as an 
        Affective Computing sensor, returning raw VAD coordinates.
        """
        prompt = (
            "Analyze the following text and return ONLY a JSON object with "
            "valence, arousal, and dominance values between -1.0 and 1.0.\n\n"
            "Valence: -1 (Negative/Hate) to 1 (Positive/Love)\n"
            "Arousal: -1 (Calm/Bored) to 1 (Excited/Angry)\n"
            "Dominance: -1 (Submissive/Fear) to 1 (Dominant/Confidence)\n\n"
            f"Text: \"{text}\""
        )
        
        # This is a placeholder for the actual LLM call
        # response = self.model_client.generate(prompt)
        # return VADVector(**json.loads(response))
        
        # For now, we fall back to heuristic for the standalone demo
        return self._heuristic_analyze(text)

    def _heuristic_analyze(self, text: str) -> VADVector:
        """
        A basic heuristic analyzer to ensure the core engine can be tested 
        without an active API key.
        """
        text = text.lower()
        v, a, d = 0.0, 0.0, 0.0

        # Simple keyword mappings (simplified for example)
        positive_words = ["great", "love", "happy", "excellent", "thanks", "amazing"]
        negative_words = ["hate", "stupid", "wrong", "bad", "angry", "fail"]
        high_arousal = ["!", "urgent", "now", "stop", "incredible", "shock"]
        dominant_words = ["must", "will", "command", "do this", "order"]
        submissive_words = ["sorry", "please", "maybe", "i think", "could you"]

        # Valence
        v += sum(0.2 for w in positive_words if w in text)
        v -= sum(0.2 for w in negative_words if w in text)
        
        # Arousal
        a += sum(0.3 for w in high_arousal if w in text)
        if "!" in text: a += 0.2
        
        # Dominance
        d += sum(0.2 for w in dominant_words if w in text)
        d -= sum(0.2 for w in submissive_words if w in text)

        return VADVector(
            valence=max(-1.0, min(1.0, v)),
            arousal=max(-1.0, min(1.0, a)),
            dominance=max(-1.0, min(1.0, d))
        )

# Integration Test
if __name__ == "__main__":
    analyzer = ToneAnalyzer()
    
    test_phrases = [
        "I absolutely love this! It is amazing!", 
        "This is a complete failure. I hate it.",
        "Could you please help me with this, if you have time?",
        "Do this immediately. No excuses."
    ]
    
    for phrase in test_phrases:
        vec = analyzer.analyze(phrase)
        print(f"Text: {phrase}\nVector: {vec}\n")
