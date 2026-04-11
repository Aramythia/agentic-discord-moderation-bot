# Project Guidelines

## Code Style
- Python 3.12 strict requirement
- Use py-cord (discord.py fork) for Discord API
- Async/await required for Discord event handlers and slash commands; not necessary for non-Discord functions and classes
- Environment variables for secrets (.env file)
- Use Google NumPy docstring format and style conventions for utility functions

## Architecture
- Single-file bot implementation in [bot.py](src/agentic_discord_moderation_bot/bot.py)
- Slash commands for user interactions
- Event listeners for bot lifecycle and messages
- LangChain/LangGraph integration planned (currently stubbed with TODOs); emphasize usage of LangChain and LangGraph, including other common AI engineering libraries only if they are best practices and widely used
- Guild-specific configuration for safe development

## Build and Test
- Install: `uv sync`
- Run: `uv run python bot.py`
- Test: `uv run pytest` (no tests yet, add async fixtures for bot components)
- Add packages: `uv add <package>` or `uv add --dev <package>`

## Conventions
- Replace hardcoded guild IDs with config management
- Add error handling and structured logging (no print statements)
- Follow async patterns in Discord-related operations

See [README.md](README.md) for setup and environment details.</content>
<parameter name="filePath">c:\Users\sebas\OneDrive\Python_Projects\agentic-discord-moderation-bot\.github\copilot-instructions.md