# Discord LLM Bot

A Discord bot that uses AWS Bedrock to respond to user messages with an AI assistant.

## Installation

This project uses `pyproject.toml` for dependency management and is compatible with UV.

```bash
# Install dependencies with UV
uv pip install -e .

# Or with pip
pip install -e .
```

## Usage

Run the bot directly:

```bash
# Using the entry point
discord-llm

# Or run the module
python -m discord_llm.bot
```

## Commands

- `!chat <your message>` - Send a message to the AI assistant and get a response
