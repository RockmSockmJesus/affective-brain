# Integration Strategy: AffectiveBrain

AffectiveBrain is designed to be a "plugin for the soul." Depending on the agent's memory architecture, it integrates in different ways:

## 1. Integrated with Advanced Memory (e.g., GBrain)
In systems with a structured knowledge graph and state management, AffectiveBrain becomes a **State Operator**.
- **Implementation:** The Mood Vector is stored as a dedicated entry in the database (e.g., `state/affective_vector`).
- **Benefit:** Emotional states can be linked to specific entities. The agent can feel "anxious" specifically when talking about a certain project, or "warm" toward a specific person, creating a nuanced social memory.

## 2. Integrated with Knowledge-Centric Systems (e.g., LLMWiki)
In systems like Karpathy's LLMWiki, where information is stored in interconnected notes, AffectiveBrain adds **Affective Metadata**.
- **Implementation:** Each wiki page or "thought" can be tagged with a VAD vector representing the emotional state the agent was in when that information was recorded.
- **Benefit:** When retrieving information, the agent doesn't just get the facts—it retrieves the *feeling* associated with them. This allows for "Emotional Retrieval," where the agent's current mood influences which memories are most salient.

## 3. Standalone / Stateless Agents
For agents with no persistent memory or simple session history, AffectiveBrain operates as a **State-Passing Middleware**.
- **Implementation:** The Mood Vector is treated as a "Session Token." The middleware calculates the new state and passes it back to the client or stores it in a lightweight cookie/cache.
- **Benefit:** Adds a layer of personality and continuity to otherwise sterile API calls without requiring a full database backend.

## Summary Table

| Architecture | Storage Mechanism | Primary Benefit |
| :--- | :--- | :--- |
| **GBrain** | Knowledge Graph / DB | Long-term emotional bonds & entity-specific moods. |
| **LLMWiki** | Page Metadata / Tags | Emotionally-weighted knowledge retrieval. |
| **Stateless** | Session Token / JSON | Consistent personality across a single conversation. |
