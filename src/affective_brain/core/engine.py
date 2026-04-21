import math
from dataclasses import dataclass, asdict
from typing import Dict, Optional
import time

@dataclass
class VADVector:
    valence: float    # -1.0 to 1.0
    arousal: float    # -1.0 to 1.0
    dominance: float  # -1.0 to 1.0

    def to_dict(self):
        return asdict(self)

class AffectiveCore:
    def __init__(
        self, 
        baseline: VADVector = VADVector(0.0, 0.0, 0.0), 
        decay_rates: Dict[str, float] = None, 
        sensitivity: float = 0.3
    ):
        self.baseline = baseline
        # Dimension-specific decay: Arousal usually fades faster than Valence (Mood)
        self.decay_rates = decay_rates or {"valence": 0.02, "arousal": 0.1, "dominance": 0.05}
        self.sensitivity = sensitivity
        self.current_state = baseline
        self.last_update_time = time.time()

    def _sigmoid(self, x: float) -> float:
        """Saturates values to prevent linear runaway and simulate emotional plateaus."""
        return 2 / (1 + math.exp(-x)) - 1

    def _apply_decay(self):
        now = time.time()
        delta_t = (now - self.last_update_time) / 60.0
        
        # Apply dimension-specific exponential decay
        def decay(current, base, rate):
            return base + (current - base) * math.exp(-rate * delta_t)

        self.current_state = VADVector(
            valence = decay(self.current_state.valence, self.baseline.valence, self.decay_rates["valence"]),
            arousal = decay(self.current_state.arousal, self.baseline.arousal, self.decay_rates["arousal"]),
            dominance = decay(self.current_state.dominance, self.baseline.dominance, self.decay_rates["dominance"])
        )
        self.last_update_time = now

    def update_state(self, stimulus: VADVector):
        self._apply_decay()
        
        # 1. Inter-Dimensional Coupling
        # High arousal (excitement/panic) tends to pull valence away from neutral
        coupling_effect = 0.1 * stimulus.arousal * (1 if stimulus.valence > 0 else -1)
        
        # 2. Weighted Blend with Saturation
        # We apply the stimulus to the current state, then pass through sigmoid to saturate
        def blend(current, stim, coupling=0):
            raw = current + (stim - current) * self.sensitivity + coupling
            return self._sigmoid(raw)

        self.current_state = VADVector(
            valence = blend(self.current_state.valence, stimulus.valence, coupling_effect),
            arousal = blend(self.current_state.arousal, stimulus.arousal),
            dominance = blend(self.current_state.dominance, stimulus.dominance)
        )

    def get_state(self) -> Dict:
        self._apply_decay()
        return self.current_state.to_dict()
