from typing import Dict, Any
from .engine import VADVector

class SoulMapper:
    \"\"\"
    Maps a high-level SOUL manifest (YAML/Dict) to mathematical constants 
    for the AffectiveCore engine.
    \"\"\"
    
    # Default personality mappings for OCEAN traits (0.0 to 1.0)
    # Neuroticism: High = higher sensitivity, slower recovery
    # Extraversion: High = higher arousal baseline, faster spikes
    # Agreeableness: High = higher valence baseline
    # Conscientiousness: High = more stable (lower sensitivity)
    # Openness: High = wider range of arousal
    
    @staticmethod
    def map_soul_to_core_params(soul: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Extract OCEAN traits or use defaults
        traits = soul.get('traits', {
            'openness': 0.5,
            'conscientiousness': 0.5,
            'extraversion': 0.5,
            'agreeableness': 0.5,
            'neuroticism': 0.5
        })
        
        # 2. Determine Baseline VAD
        # Base valence influenced by Agreeableness
        baseline_v = (traits['agreeableness'] - 0.5) * 0.4
        # Base arousal influenced by Extraversion
        baseline_a = (traits['extraversion'] - 0.5) * 0.4
        # Base dominance influenced by a mix of Extraversion and Conscientiousness
        baseline_d = ((traits['extraversion'] + traits['conscientiousness']) / 2 - 0.5) * 0.4
        
        # 3. Determine Sensitivity (Volatility)
        # High Neuroticism = High Sensitivity
        # High Conscientiousness = Low Sensitivity (emotional stability)
        sensitivity = 0.2 + (traits['neuroticism'] * 0.3) - (traits['conscientiousness'] * 0.1)
        sensitivity = max(0.1, min(0.8, sensitivity))
        
        # 4. Determine Decay Rates (Recovery Speed)
        # High Neuroticism = Slower recovery (higher persistence of negative states)
        # recovery_multiplier > 1 means slower decay
        recovery_multiplier = 0.5 + traits['neuroticism'] 
        
        decay_rates = {
            \"valence\": 0.02 / recovery_multiplier,
            \"arousal\": 0.1 / recovery_multiplier,
            \"dominance\": 0.05 / recovery_multiplier
        }
        
        return {
            \"baseline\": VADVector(baseline_v, baseline_a, baseline_d),
            \"sensitivity\": sensitivity,
            \"decay_rates\": decay_rates
        }
