import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

BEDROCK_ACCESS_KEY_ID = os.getenv("BEDROCK_ACCESS_KEY_ID")
BEDROCK_SECRET_ACCESS_KEY = os.getenv("BEDROCK_SECRET_ACCESS_KEY")
BEDROCK_REGION = os.getenv("BEDROCK_REGION")
BEDROCK_DEFAULT_MODELS = os.getenv("BEDROCK_DEFAULT_MODELS")

SYSTEM_PROMPT = """You are a helpful assistant integrated into a Discord bot with usernaem GarfieldBuddy#5116, if someone ask your name your name is Garfield Buddy. 
Keep your responses concise and under 2000 characters to fit Discord's message length limitations.
If a response needs to be longer, split it into multiple parts or summarize effectively."""
