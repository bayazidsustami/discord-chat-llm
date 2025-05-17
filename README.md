# Discord LLM Bot

A Discord bot that uses AWS Bedrock to respond to user messages with an AI assistant and generate images.

## Features

- AI chat responses when the bot is mentioned in a channel
- Direct message chat support
- Image generation with various artistic styles
- Garfield-themed commands including jokes, facts, quotes, and more

## Installation

This project uses `pyproject.toml` for dependency management and is compatible with UV.

```bash
# Install dependencies with UV
uv pip install -e .

# Or with pip
pip install -e .
```

## Configuration

Create a `.env` file in the root directory with the following variables:

```
DISCORD_TOKEN=your_discord_bot_token
BEDROCK_ACCESS_KEY_ID=your_aws_access_key
BEDROCK_SECRET_ACCESS_KEY=your_aws_secret_key
BEDROCK_REGION=your_aws_region
BEDROCK_DEFAULT_MODELS=your_preferred_model_id
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

### Chat

- Mention the bot in a channel: `@BotName your message` - Get a response from the AI
- Send a direct message to the bot - Have a private conversation with the AI

### Image Generation

- `/image <prompt>` - Generate an image based on a prompt
- `/image <style>: <prompt>` - Generate an image with a specific style (e.g., `/image pixel-art: a house`)
- `/image-styles` - Show available image generation styles

### Garfield-themed Commands

- `/fact` - Get a random Garfield fact
- `/quote` - Get a random Garfield quote
- `/lasagna` - Get a lasagna recipe
- `/joke` - Get a Garfield-style joke
- `/monday` - Express Garfield's feelings about Mondays

### Utility Commands

- `/help` - Show all available commands and how to use them
- `/about` - Show information about this bot
- `/ping` - Check if the bot is online

## Deployment

This project includes a GitHub Actions workflow for automatic deployment to a server.

## Contributing

We welcome contributions to improve Discord LLM Bot! Here's how you can contribute:

1. **Fork the Repository**
   - Fork this repository to your GitHub account

2. **Clone the Fork**
   ```bash
   git clone https://github.com/bayazidsustami/discord-chat-llm.git
   cd discord-llm
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Implement your feature or bug fix
   - Add or update tests as necessary
   - Update documentation to reflect your changes

5. **Run Tests**
   ```bash
   pytest
   ```

6. **Commit Your Changes**
   ```bash
   git commit -m "Add feature: your feature description"
   ```

7. **Push to GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Submit a Pull Request**
   - Go to the repository on GitHub
   - Click on "Pull Request" and then "New Pull Request"
   - Select your branch and submit the pull request with a clear description of the changes

9. **Code Review**
   - Wait for the maintainers to review your PR
   - Make any requested changes

### Coding Standards

- Follow PEP 8 style guidelines for Python code
- Write docstrings for all functions, classes, and methods
- Include type hints where appropriate
- Add unit tests for new functionality

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
