---
name: Add Discord Slash Command
description: "Generate or update one py-cord slash command using explicit command metadata and testable wrapper architecture."
argument-hint: "Command name, purpose, parameters, response behavior, and optional AI behavior"
agent: agent
---

Create or update exactly one py-cord slash command in this repository.

Follow project guidance from [workspace instructions](../copilot-instructions.md) and [Discord bot skill](../skills/discord-bot-development/SKILL.md).

Requirements:
- Use async/await for the Discord command handler.
- Define slash command metadata explicitly:
  - Always set the command name kwarg in the decorator.
  - Always set a clear command description.
  - Ensure parameters are well-defined via options.
- Prefer option decorators for readability when declaring options.
- Keep the slash command handler as a thin Discord wrapper.
- Move business logic into generic Python functions so it can be unit-tested.
- Favor ctx.reply over ctx.respond when applicable.
- If AI behavior is included, use LangChain/LangGraph-first patterns and avoid niche dependencies unless best practice and widely adopted.
- Add or update Google NumPy-style docstrings for utility functions created or changed.

Output format:
1. Files changed.
2. Final slash command signature and options summary.
3. Generic function(s) extracted for testability.
4. Suggested async pytest test cases.
5. Risks or follow-up items.
