---
name: discord-bot-development
description: "Use when: adding or updating Discord slash commands, event handlers, moderation logic, LangChain/LangGraph integrations, or async tests in this repository. Includes patterns for py-cord async handlers, AI workflow integration, config usage, and utility docstring style."
---

# Discord Bot Development

## Purpose
Use this skill for multi-step Discord bot work in this repository, especially when tasks touch slash commands, event handlers, AI orchestration, or test scaffolding.

## Project Context
- Runtime: Python 3.12
- Discord framework: py-cord
- Dependency manager: uv
- Main bot implementation: src/agentic_discord_moderation_bot/bot.py
- Workspace instructions: .github/copilot-instructions.md

## When To Use
- Add or modify slash commands.
- Update Discord lifecycle or message event handlers.
- Integrate or refactor LangChain and LangGraph workflow code.
- Introduce utility helpers that support bot moderation flows.
- Add or update async pytest coverage for bot behaviors.

## Required Conventions
- Use async/await for Discord event handlers and slash commands.
- Non-Discord utility functions and classes may be synchronous when appropriate.
- Prefer environment-based configuration and avoid hardcoded secrets.
- Use LangChain and LangGraph by default for AI orchestration tasks.
- Add other AI libraries only when they are best practice and widely adopted.
- For utility functions, write Google NumPy-style docstrings.
- For slash commands, always define explicit options and a command description.
- Populate the slash command name kwarg explicitly so Python function names can be changed safely.
- Prefer defining options with option decorators for readability.
- Keep slash commands as wrappers over generic Python functions so business logic is unit-testable.
- Favor ctx.reply over ctx.respond when applicable.

## Command And Handler Pattern
Use this pattern when generating command handlers:
1. Validate input early and return user-safe feedback.
2. Define slash command metadata explicitly (name, description, options) and keep option declarations readable.
3. Keep Discord interaction code thin.
4. Delegate reusable logic into utility functions or service-layer functions.
5. Call generic Python functions from command wrappers to enable unit testing without Discord runtime.
6. Prefer ctx.reply where Discord context allows it.
7. Wrap AI calls with defensive error handling.
8. Log failures with actionable context.

## AI Integration Pattern
When adding AI behavior:
1. Keep prompt construction isolated from Discord transport code.
2. Put model/tool orchestration in dedicated helper functions.
3. Keep LangGraph state and transitions explicit.
4. Add clear TODO markers only for unresolved architecture decisions.
5. Avoid adding niche dependencies if LangChain/LangGraph already solve the need.

## Testing Workflow
Use this approach for test additions:
1. Create async tests with pytest for slash command and handler logic.
2. Isolate Discord objects behind fixtures/mocks.
3. Prioritize tests for moderation policy branches and AI fallback behavior.
4. Run tests with: uv run pytest

## Suggested Execution Steps
For implementation tasks, follow this sequence:
1. Read related code in src/agentic_discord_moderation_bot/bot.py.
2. Implement the smallest safe change.
3. Update or add utility docstrings in Google NumPy style.
4. Run targeted checks or tests where available.
5. Summarize behavior changes and residual risks.

## Output Checklist
Before finishing, verify:
- Async Discord handlers remain correct.
- AI integration uses LangChain/LangGraph-first decisions.
- Utility docstrings follow Google NumPy conventions.
- No secrets were added to source files.
- Commands used match project tooling (uv).
