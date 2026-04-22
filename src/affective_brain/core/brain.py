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
        
        # 1. Initialize Soul and Core
        if soul_config:
            self.soul = soul_config
            self._calibrate_from_soul()
        else:
            saved_soul = self.persistence.load_soul()
            if saved_soul:
                self.soul = saved_soul
                self._calibrate_from_soul()
            else:
                self.soul = {"resting_mood": "neutral", "core_values": "neutral", "traits": {}}
                self._calibrate_from_soul()
        
        self.appraisal = AppraisalEngine(self.soul)
        self.expression_filter = ExpressionFilter(self.soul)
        self.modulator = MoodModulator()
        
        # Load last known emotional state
        saved_state = self.persistence.load_state()
        if saved_state:
            self.core.current_state = VADVector(**saved_state)
            self.core.last_update_time = saved_state.get("timestamp", time.time())

    def _calibrate_from_soul(self):
        from .soul_mapper import SoulMapper
        params = SoulMapper.map_soul_to_core_params(self.soul)
        self.core = AffectiveCore(
            baseline=params['baseline'],
            sensitivity=params['sensitivity'],
            decay_rates=params['decay_rates']
        )

    def get_psych_report(self) -> Dict[str, Any]:
        \"\"\"
        Returns a comprehensive psychological snapshot of the agent's internal state.
        This is the 'glass box' view of the soul.
        \"\"\"
        raw_state = self.core.get_state()
        filtered_state = self.expression_filter.filter_state(raw_state)
        
        # Calculate the 'Honesty Gap' (difference between raw and filtered)
        honesty_gap = {
            dim: abs(raw_state[dim] - filtered_state[dim]) 
            for dim in raw_state
        }
        
        return {
            "internal_state": raw_state,
            "expressed_state": filtered_state,
            "honesty_gap": honesty_gap,
            "drives": {name: drive.value for name, drive in self.core.drives.items()},
            "masking_factor": self.expression_filter.masking_factor,
            "active_triggers": list(self.core.triggers.keys()),
            "status": "Stable" if max(honesty_gap.values()) < 0.3 else "Masking Heavy Emotion"
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
