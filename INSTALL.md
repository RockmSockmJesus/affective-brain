# Installation Guide: AffectiveBrain 🧠

AffectiveBrain is a plug-and-play affective computing layer. Follow these steps to integrate it into your AI agent.

## 🚀 Quick Start

### 1. Install the Package
If installing from source:
```bash
git clone https://github.com/your-repo/affective-brain.git
cd affective-brain
pip install .
```

### 2. Basic Implementation
Here is the simplest way to add emotional intelligence to your agent:

```python
from affective_brain import AffectiveBrain

# Initialize the brain (will look for data/soul.json)
brain = AffectiveBrain(storage_dir="my_agent_data")

# If it's a new agent, run onboarding
# brain.run_onboarding(user_answers) 

# In your agent's message loop:
user_input = "I can't believe you forgot the deadline!"
result = brain.process_input(user_input)

# Inject the constraints into your LLM system prompt
system_prompt = f"You are a helpful assistant. {result['constraints']}"
# response = llm.generate(system_prompt, user_input)
```

## 🛠 Integration Options

### For Stateless Agents
Pass the `state` dictionary as metadata in your request and load it back into the brain using `persistence.load_state()` at the start of the next turn.

### For Knowledge-Graph Agents (e.g., GBrain/LLMWiki)
Store the `VADVector` as an attribute of a "Memory" or "Page" object. When retrieving a memory, use the stored VAD vector to shift the agent's current mood, creating "Emotional Recall."
