# agentic-discord-moderation-bot

A Discord bot with agentic AI capabilities using LangChain and LangGraph.

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

### Prerequisites

- Python 3.12
- uv installed

### Installation

1. Install uv if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone or navigate to the project directory.

3. Install dependencies:
   ```bash
   uv sync
   ```

4. Activate the virtual environment:
   ```bash
   uv run python --version
   ```

### Usage

Run the bot:
```bash
uv run python bot.py
```

### Development

To add new dependencies:
```bash
uv add <package-name>
```

For dev dependencies:
```bash
uv add --dev <package-name>
```