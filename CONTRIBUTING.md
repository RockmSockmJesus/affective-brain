# Contributing to AffectiveBrain 🤝

We welcome contributions to help make AI agents feel more human. AffectiveBrain is built on the Valence-Arousal-Dominance (VAD) model, and we are looking for help in making the "simulation" more nuanced.

## 🌈 How You Can Contribute

### 1. Expand the `SoulMapper`
The current mapping from natural language (e.g., "Stoic") to VAD constants is a starting point. We need more diverse personality archetypes.
- **Task:** Add new keywords and their corresponding VAD offsets to `soul_mapper.py`.

### 2. Enhance the `ToneAnalyzer`
The current analyzer uses heuristics. We want to integrate more robust, multimodal detection.
- **Task:** Implement a `ModelAnalyzer` that uses a small, fast LLM or a dedicated sentiment model to produce high-precision VAD vectors.

### 3. Refine the `MoodModulator`
The "Voice Constraints" can be expanded to include more subtle linguistic cues.
- **Task:** Add rules for punctuation, sentence length, and specific word choices based on the Arousal and Dominance axes.

### 4. New "Personality Templates"
Create pre-defined SOUL documents for common archetypes (e.g., "The Grumpy Professor," "The Eager Intern").

## 🛠 Development Workflow

1. **Fork** the repository.
2. **Create a branch** for your feature: `git checkout -b feature/new-personality`.
3. **Implement** your changes in `src/affective_brain/core/`.
4. **Test** your changes using the `examples/` scripts to ensure the mood shifts as expected.
5. **Submit a Pull Request** with a description of how the change affects the agent's "feel."

## 📜 The VAD Standard
When contributing, please stick to the VAD coordinates:
- **Valence:** -1.0 (Hate/Pain) $\rightarrow$ 1.0 (Love/Joy)
- **Arousal:** -1.0 (Sleep/Calm) $\rightarrow$ 1.0 (Panic/Excitement)
- **Dominance:** -1.0 (Submissive) $\rightarrow$ 1.0 (Dominant)
