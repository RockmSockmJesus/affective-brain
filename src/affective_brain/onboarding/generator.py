import json
import os
from typing import Dict, Any, List

class SoulScribe:
    """
    The SoulScribe is an interactive onboarding system that conducts a 
    'Psychological Intake Interview' to generate a SOUL manifest.
    """
    
    def __init__(self, storage_dir: str = "data"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        
        # The interview script: trait -> question
        self.interview_questions = [
            {
                "trait": "openness",
                "question": "Do you prefer sticking to established routines and known truths, or are you drawn to abstract ideas and unconventional experiences?",
                "options": ["Routine/Concrete", "Abstract/Experimental"]
            },
            {
                "trait": "conscientiousness",
                "question": "When approaching a task, are you more focused on strict organization and precision, or do you prefer a flexible, spontaneous approach?",
                "options": ["Organized/Precise", "Flexible/Spontaneous"]
            },
            {
                "trait": "extraversion",
                "question": "Do you find energy through active engagement and external stimulation, or do you prefer internal reflection and quiet observation?",
                "options": ["Active/Engaged", "Reflective/Quiet"]
            },
            {
                "trait": "agreeableness",
                "question": "In a conflict, is your primary instinct to maintain harmony and cooperation, or to prioritize challenge and critical analysis?",
                "options": ["Harmony/Cooperation", "Challenge/Analysis"]
            },
            {
                "trait": "neuroticism",
                "question": "How do you typically react to unexpected stress? Do you tend to feel the impact deeply and for a duration, or do you recover your equilibrium quickly?",
                "options": ["Deeply/Persistent", "Quickly/Stable"]
            }
        ]

    def conduct_interview(self) -> Dict[str, Any]:
        """
        Simulates an interactive interview. In a real CLI, this would use input().
        Returns a populated SOUL manifest.
        """
        print("--- AffectiveBrain: Psychological Intake Interview ---")
        print("Please answer the following to calibrate your emotional baseline.\n")
        
        traits = {}
        for q in self.interview_questions:
            print(f"{q['question']}")
            for i, opt in enumerate(q['options']):
                print(f" {i+1}. {opt}")
            
            # In a real environment, we'd use input(). 
            # For this implementation, we provide a method to pass answers.
            choice = input("Selection (1 or 2): ")
            # Map 1 -> 0.0, 2 -> 1.0 (or vice versa depending on trait)
            # For simplicity: 1 is 'Low', 2 is 'High' for the trait's standard definition
            traits[q['trait']] = 0.0 if choice == "1" else 1.0
            print("-" * 30)
            
        return {
            "name": "New Soul",
            "traits": traits,
            "baseline_pad": {"v": 0.0, "a": 0.0, "d": 0.0}, # Calculated by SoulMapper
            "core_values": "General Utility"
        }

    def save_soul(self, soul_data: Dict[str, Any], name: str = "default_soul"):
        path = os.path.join(self.storage_dir, f"{name}.json")
        with open(path, 'w') as f:
            json.dump(soul_data, f, indent=4)
        print(f"Soul manifest saved to {path}")

if __name__ == "__main__":
    scribe = SoulScribe()
    # This would be called by the agent onboarding flow
    # soul = scribe.conduct_interview()
    # scribe.save_soul(soul)
