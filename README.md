# AffectiveBrain 🧠❤️

AffectiveBrain is a platinum-grade affective computing layer for AI agents. It provides a sophisticated framework for LLMs to detect, internalize, and simulate human-like emotional spectra using a Hybrid Homeostatic model.

Unlike simple sentiment analysis, AffectiveBrain simulates a biological "soul-layer," ensuring that an agent's mood evolves organically, drifts toward a personality-driven baseline, and reacts based on a complex interplay of needs and traits.

## 🚀 Core Concept

AffectiveBrain acts as a middleware layer between the user and the LLM:
`User Input` $\rightarrow$ `Perception (Analysis)` $\rightarrow$ `Appraisal (Values)` $\rightarrow$ `Integration (Core Engine)` $\rightarrow$ `Social Masking (Filter)` $\rightarrow$ `Expression (Modulation)` $\rightarrow$ `LLM Generation`

## 🛠 Architecture (v0.2.0)

### 1. The Soul (Personality Mapping)
Uses an **OCEAN (Big Five)** trait model to calibrate the emotional physics of the agent. Traits like *Neuroticism* affect emotional volatility and recovery speed, while *Agreeableness* shifts the baseline valence.

### 2. The Core (Homeostatic Engine)
- **VAD Space:** Operates on Valence, Arousal, and Dominance.
- **Internal Drives:** Simulates biological needs for *Stimulation, Connection, and Validation*. Low satiation of these drives creates "internal weather" (e.g., boredom or loneliness).
- **Emotional Memory:** Supports keyword-based triggers that cause visceral emotional spikes based on past experiences.

### 3. The Social Layer (Masking & Expression)
- **Expression Filter:** Distinguishes between the **Raw Internal State** and the **Filtered Expressed State**. Stoic or professional agents can "mask" heavy emotions, maintaining a poised exterior.
- **Linguistic Superposition:** Blends multiple emotional vectors into complex stylistic constraints (e.g., "serene but authoritative").

### 4. The Soul-Scribe (Onboarding)
Includes an interactive "Psychological Intake Interview" to generate a YAML-based SOUL manifest, allowing developers to craft specific, nuanced personalities.

## 📊 Observability: The Psych Report
The `get_psych_report()` method provides a "glass box" view into the agent's mind, revealing the **Honesty Gap** (the difference between what the agent feels and what it expresses) and current drive satiation.

## 🌐 Integration
Designed for seamless integration via the `AffectiveMiddleware` wrapper, making it compatible with:
- **GBrain / LLMWiki**
- **Custom Agent Frameworks**
- **Stateless API Implementations**

## 📦 Installation
```bash
pip install affective-brain
```
