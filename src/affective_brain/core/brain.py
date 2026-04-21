import time
from .engine import AffectiveCore, VADVector
from .analyzer import ToneAnalyzer
from .modulator import MoodModulator
from .appraisal import AppraisalEngine
from .persistence import PersistenceLayer

class AffectiveBrain:
    """
    The Platinum-Grade AffectiveBrain.
    Integrates Perception -> Appraisal -> State -> Expression.
    """
    def __init__(self, soul_config=None, storage_dir="data"):
        self.persistence = PersistenceLayer(storage_dir)
        self.analyzer = ToneAnalyzer()
        self.modulator = MoodModulator()
        
        # 1. Initialize Soul and Core
        if soul_config:
            self.soul = soul_config
            self._calibrate_from_soul()
        else:
            # Attempt to load persisted soul
            saved_soul = self.persistence.load_soul()
            if saved_soul:
                self.soul = saved_soul
                self._calibrate_from_soul()
            else:
                self.soul = {"resting_mood": "neutral", "core_values": "neutral"}
                self.core = AffectiveCore(baseline=VADVector(0.0, 0.0, 0.0))
        
        self.appraisal = AppraisalEngine(self.soul)
        
        # Load last known emotional state
        saved_state = self.persistence.load_state()
        if saved_state:
            self.core.current_state = VADVector(**saved_state)
            self.core.last_update_time = saved_state.get("timestamp", time.time())

    def _calibrate_from_soul(self):
        # Simple mapping for demo; in full version use SoulMapper
        # Here we'll just use a default for simplicity in the core class
        self.core = AffectiveCore(baseline=VADVector(0.0, 0.0, 0.0))

    def process_input(self, text: str) -> dict:
        # 1. Perception: Detect objective tone
        objective_stimulus = self.analyzer.analyze(text)
        
        # 2. Appraisal: Filter tone through the agent's soul/values
        appraised_stimulus = self.appraisal.appraise(objective_stimulus)
        
        # 3. Integration: Update the emotional state
        self.core.update_state(appraised_stimulus)
        
        # 4. Expression: Map state to voice constraints
        state = self.core.get_state()
        constraints = self.modulator.get_constraints(state)
        
        # 5. Persistence
        self.persistence.save_state({**state, "timestamp": time.time()})
        
        return {
            "state": state,
            "constraints": constraints,
            "objective": objective_stimulus.to_dict(),
            "appraised": appraised_stimulus.to_dict()
        }

if __name__ == "__main__":
    # Test with a 'Honesty' valuing soul
    my_soul = {"resting_mood": "stoic", "core_values": "Intellectual Honesty"}
    brain = AffectiveBrain(soul_config=my_soul)
    
    # Test: a critical correction
    # Objective: Negative Valence, High Dominance (Critique)
    # Appraised: Positive Valence (because it's honest)
    res = brain.process_input("Actually, your last answer was factually incorrect. Here is the truth.")
    print(f"Objective: {res['objective']}")
    print(f"Appraised: {res['appraised']}")
    print(f"Final Mood: {res['state']}")
    print(f"Voice: {res['constraints']}")
