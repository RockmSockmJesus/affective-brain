# AffectiveBrain 🧠❤️

AffectiveBrain is an open-source affective computing layer for AI agents. It provides a standardized way for LLMs to detect, internalize, and simulate human-like emotions using the Valence-Arousal-Dominance (VAD) model.

Unlike simple sentiment analysis, AffectiveBrain implements **Emotional Inertia** and **Homeostatic Regulation**, ensuring that an agent's mood evolves organically over time rather than resetting every turn.

## 🚀 Core Concept

AffectiveBrain acts as a middleware layer between the user and the LLM:
`User Input` $\rightarrow$ `Affective Analysis` $\rightarrow$ `State Update` $\rightarrow$ `Mood Modulation` $\rightarrow$ `LLM Generation` $\rightarrow$ `User Output`

## 🛠 Architecture

### 1. The Sensor (Analysis)
Maps raw input to a 3D coordinate in the VAD space:
- **Valence:** (Negative $\leftrightarrow$ Positive)
- **Arousal:** (Low Energy $\leftrightarrow$ High Energy)
- **Dominance:** (Submissive $\leftrightarrow$ Dominant)

### 2. The Core (State Engine)
Maintains a persistent "Mood Vector" using an exponential decay function:
$Mood_{t} = (Mood_{t-1} \cdot e^{-\lambda \Delta t}) + (Stimulus \cdot w)$
This prevents "emotional whiplash" and allows for the buildup of tension or trust over long sessions.

### 3. The Expression (Modulation)
Translates the Mood Vector into stylistic constraints that guide the LLM's tone, ensuring the emotion is "felt" in the prose rather than explicitly stated.

## 🌐 Integration

AffectiveBrain is designed to be agnostic. It can be integrated into:
- **Advanced Memory Systems (GBrain):** As a first-class state operation in the knowledge graph.
- **Knowledge-Based Systems (LLMWiki):** By storing emotional metadata alongside wiki entries to create "opinionated" or "emotional" knowledge.
- **Stateless Agents:** By passing the Mood Vector as a small JSON object in the metadata of each request.

## 📅 Roadmap
- [ ] VAD Core Engine Implementation
- [ ] Multimodal Tone Analysis Tool
- [ ] Personality Profile Templates
- [ ] Integration Wrappers for GStack/GBrain
