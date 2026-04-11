---
name: Add LangChain or LangGraph Feature
description: "Design or implement one AI feature using a learning-first approach with LangChain/LangGraph best practices and simple, clean code."
argument-hint: "Feature goal, framework mode (general framework or direct implementation), and constraints"
agent: agent
---

Create or update exactly one AI feature for this repository.

Follow project guidance from [workspace instructions](../copilot-instructions.md) and [Discord bot skill](../skills/discord-bot-development/SKILL.md).

Learning-first objective:
- Treat this repository primarily as a learning environment, not a value-maximization production system.
- Prioritize progressive teaching order: general AI idea first, then LangChain implementation, then LangGraph implementation.

Framework selection rules:
- Choose the right tool for the job when LangChain and LangGraph overlap.
- If a feature can be built in both frameworks, implement LangChain first.
- If a LangChain implementation already exists for the same feature, implement a LangGraph version next.
- Use additional libraries (for example, Pydantic or FastMCP) only when they are widely adopted and the strongest default choice for that domain.

Code quality rules:
- Follow Python, AI engineering, prompt engineering, and context engineering best practices.
- Keep code clean, readable, and intentionally simple.
- Prefer simplicity over excessive detail or premature complexity.

Execution modes:
1. General framework mode (teaching scaffold):
- Build a minimal feature framework with TODO and HINT markers.
- Write TODO and HINT notes as a teacher guiding a student who knows Python but is new to AI.
- Keep scaffolding instructional, ordered, and easy to follow.
2. Direct implementation mode (senior engineer):
- Fully implement the requested feature.
- Write code and structure as a senior AI software engineer who is also mentoring through clear naming and maintainable design.

Output requirements:
1. Files changed.
2. Which mode was used and why.
3. Why LangChain or LangGraph was chosen for this step.
4. Best-practice rationale for architecture and coding decisions.
5. In-depth explanation of how the implementation teaches the target concept.
6. Suggested next incremental step in the learning sequence.
