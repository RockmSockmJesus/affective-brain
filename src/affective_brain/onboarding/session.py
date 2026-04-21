import random
from typing import List, Dict
from .generator import PersonalityGenerator

class OnboardingSession:
    """
    Handles the psychological intake interview or the 'Genesis' randomization.
    """
    def __init__(self):
        self.questions = [
            {
                "id": "resting_mood",
                "text": "If your agent were a person sitting in a quiet room, what is their natural 'resting' mood? (e.g., Stoic, Melancholic, Cheerful, Anxious)",
                "impact": "baseline"
            },
            {
                "id": "emotional_stability",
                "text": "How quickly does your agent bounce back from a negative interaction? (e.g., Fast/Resilient, Slow/Lingering, Volatile/Extreme)",
                "impact": "decay_rate"
            },
            {
                "id": "sensitivity",
                "text": "How strongly does the agent react to the user's tone? (e.g., Thin-skinned/High-reactivity, Thick-skinned/Unfazed)",
                "impact": "sensitivity"
            },
            {
                "id": "power_dynamic",
                "text": "In the relationship with the user, is the agent a humble servant, an equal partner, or a confident mentor/authority?",
                "impact": "baseline_dominance"
            },
            {
                "id": "core_values",
                "text": "What is one thing this agent values above all else? (e.g., Honesty, Efficiency, Kindness, Logic)",
                "impact": "triggers"
            }
        ]
        self.answers = {}

    def get_question(self, index: int) -> str:
        return self.questions[index]["text"]

    def save_answer(self, index: int, answer: str):
        q_id = self.questions[index]["id"]
        self.answers[q_id] = answer

    def synthesize_soul(self) -> str:
        soul_md = "# SOUL DOCUMENT\n\n"
        soul_md += "## Identity Profile\n"
        for q in self.questions:
            q_id = q["id"]
            ans = self.answers.get(q_id, "Not specified")
            soul_md += f"- **{q_id.replace('_', ' ').title()}:** {ans}\n"
        
        soul_md += "\n## Affective Parameters\n"
        soul_md += "This document serves as the ground truth for the AffectiveBrain's VAD constants."
        return soul_md

    def genesis_mode(self) -> Dict:
        """
        Generates a random personality based on the human bell curve.
        """
        return PersonalityGenerator.generate_random_soul()
