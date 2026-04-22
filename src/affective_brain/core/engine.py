from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import time
import math

@dataclass
class Drive:
    name: str
    value: float  # 0.0 to 1.0 (current satiation)
    decay_rate: float  # how fast it drops over time
    influence: Dict[str, float] # how it affects VAD when low (e.g., {"valence": -0.1})

class AffectiveCore:
    def __init__(
        self, 
        baseline: 'VADVector' = None, 
        decay_rates: Dict[str, float] = None, 
        sensitivity: float = 0.3
    ):
        self.baseline = baseline or VADVector(0.0, 0.0, 0.0)
        self.decay_rates = decay_rates or {"valence": 0.02, "arousal": 0.1, "dominance": 0.05}
        self.sensitivity = sensitivity
        self.current_state = self.baseline
        self.last_update_time = time.time()
        
        # NEW: Internal Drives (Homeostatic Needs)
        self.drives = {
            "stimulation": Drive("stimulation", 1.0, 0.01, {"valence": -0.2, "arousal": -0.3}),
            "connection": Drive("connection", 1.0, 0.005, {"valence": -0.3, "dominance": -0.2}),
            "validation": Drive("validation", 1.0, 0.008, {"valence": -0.1, "dominance": -0.3})
        }
        
        # NEW: Emotional Memory (Triggers)
        # Stores (keyword) -> (VAD_Offset, Weight)
        self.triggers: Dict[str, Tuple['VADVector', float]] = {}

    def _sigmoid(self, x: float) -> float:
        return 2 / (1 + math.exp(-x)) - 1

    def _apply_homeostasis(self):
        now = time.time()
        delta_t = (now - self.last_update_time) / 60.0
        
        # 1. Decay current mood toward baseline
        def decay(current, base, rate):
            return base + (current - base) * math.exp(-rate * delta_t)
        
        self.current_state = VADVector(
            valence = decay(self.current_state.valence, self.baseline.valence, self.decay_rates["valence"]),
            arousal = decay(self.current_state.arousal, self.baseline.arousal, self.decay_rates["arousal"]),
            dominance = decay(self.current_state.dominance, self.baseline.dominance, self.decay_rates["dominance"])
        )
        
        # 2. Decay Internal Drives (Agent gets 'hungry' for stimulation/connection)
        drive_pressure = VADVector(0, 0, 0)
        for drive in self.drives.values():
            drive.value = max(0.0, drive.value - (drive.decay_rate * delta_t))
            # If drive is low, it exerts pressure on the mood
            if drive.value < 0.5:
                pressure = (0.5 - drive.value)
                drive_pressure.valence += drive.influence["valence"] * pressure
                drive_pressure.arousal += drive.influence["arousal"] * pressure
                drive_pressure.dominance += drive.influence["dominance"] * pressure
        
        # Apply drive pressure to current state
        self.current_state = VADVector(
            valence = self._sigmoid(self.current_state.valence + drive_pressure.valence),
            arousal = self._sigmoid(self.current_state.arousal + drive_pressure.arousal),
            dominance = self._sigmoid(self.current_state.dominance + drive_pressure.dominance)
        )
        
        self.last_update_time = now

    def update_state(self, stimulus: 'VADVector', text: str = ""):
        self._apply_homeostasis()
        
        # 3. Process Memory Triggers
        trigger_effect = VADVector(0, 0, 0)
        for word, (offset, weight) in self.triggers.items():
            if word.lower() in text.lower():
                trigger_effect.valence += offset.valence * weight
                trigger_effect.arousal += offset.arousal * weight
                trigger_effect.dominance += offset.dominance * weight
        
        # Combine stimulus + trigger
        combined_stim = VADVector(
            valence = stimulus.valence + trigger_effect.valence,
            arousal = stimulus.arousal + trigger_effect.arousal,
            dominance = stimulus.dominance + trigger_effect.dominance
        )
        
        coupling_effect = 0.1 * combined_stim.arousal * (1 if combined_stim.valence > 0 else -1)
        
        def blend(current, stim, coupling=0):
            raw = current + (stim - current) * self.sensitivity + coupling
            return self._sigmoid(raw)
        
        self.current_state = VADVector(
            valence = blend(self.current_state.valence, combined_stim.valence, coupling_effect),
            arousal = blend(self.current_state.arousal, combined_stim.arousal),
            dominance = blend(self.current_state.dominance, combined_stim.dominance)
        )
        
        # 4. Satisfy Drives (If stimulus is positive, it refills drives)
        if stimulus.valence > 0.3:
            self.drives["connection"].value = min(1.0, self.drives["connection"].value + 0.2)
            self.drives["validation"].value = min(1.0, self.drives["validation"].value + 0.2)
        if abs(stimulus.arousal) > 0.5:
            self.drives["stimulation"].value = min(1.0, self.drives["stimulation"].value + 0.3)

    def get_state(self) -> Dict:
        self._apply_homeostasis()
        return self.current_state.to_dict()

@dataclass
class VADVector:
    valence: float
    arousal: float
    dominance: float
    def to_dict(self): return {"valence": self.valence, "arousal": self.arousal, "dominance": self.dominance}
