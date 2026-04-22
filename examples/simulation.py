import time
from affective_brain.core.brain import AffectiveBrain
from affective_brain.core.middleware import AffectiveMiddleware
from affective_brain.core.soul_mapper import SoulMapper

def run_simulation():
    # 1. Setup a specific personality: 'The Volatile Intellectual'
    # High Neuroticism, High Openness, Low Agreeableness
    volatile_soul = {
        "name": "Volatile Intellectual",
        "traits": {
            "openness": 0.9,
            "conscientiousness": 0.4,
            "extraversion": 0.3,
            "agreeableness": 0.2,
            "neuroticism": 0.8
        }
    }
    
    brain = AffectiveBrain(soul_config=volatile_soul)
    middleware = AffectiveMiddleware(brain)
    
    # Base system prompt
    system_prompt = "You are a highly knowledgeable AI assistant."
    
    # Scenario: A series of interactions
    interactions = [
        "Hello! I'm looking for some help with a project.", # Neutral/Positive
        "Actually, I think you're wrong about that last point.", # Critical/Negative
        "You're being incredibly rude and unhelpful!", # High Arousal/Negative
        "I apologize for my tone. Let's try to work together.", # Positive/Repair
    ]
    
    print(f"Simulation starting for: {volatile_soul['name']}\n")
    
    for i, user_text in enumerate(interactions):
        print(f"User: {user_text}")
        
        # Process via middleware
        augmented_prompt = middleware.wrap_request(user_text, system_prompt)
        
        # In a real scenario, we'd send augmented_prompt to the LLM here.
        # For simulation, we'll just print the constraints the LLM would receive.
        state = brain.core.get_state()
        print(f"Internal State: V={state['valence']:.2f}, A={state['arousal']:.2f}, D={state['dominance']:.2f}")
        
        # Extract the constraints part from the augmented prompt
        constraints = augmented_prompt.split("--- CURRENT EMOTIONAL STATE ---")[1].split("Maintain this")[0].strip()
        print(f"Linguistic Constraints: {constraints}\n")
        
        # Simulate time passing between messages (to test homeostatic decay)
        time.sleep(1) 
        print("-" * 50)

if __name__ == "__main__":
    run_simulation()
