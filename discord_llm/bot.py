import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import boto3
import json

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
BEDROCK_ACCESS_KEY_ID = os.getenv("BEDROCK_ACCESS_KEY_ID")
BEDROCK_SECRET_ACCESS_KEY = os.getenv("BEDROCK_SECRET_ACCESS_KEY")
BEDROCK_REGION = os.getenv("BEDROCK_REGION")
BEDROCK_DEFAULT_MODELS = os.getenv("BEDROCK_DEFAULT_MODELS")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name=BEDROCK_REGION,
    aws_access_key_id=BEDROCK_ACCESS_KEY_ID,
    aws_secret_access_key=BEDROCK_SECRET_ACCESS_KEY,
)

SYSTEM_PROMPT = """You are a helpful assistant integrated into a Discord bot. 
Keep your responses concise and under 2000 characters to fit Discord's message length limitations.
If a response needs to be longer, split it into multiple parts or summarize effectively."""

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    print(f"Bot is connected to guild ID: {GUILD_ID}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    await bot.process_commands(message)

@bot.command(name="chat")
async def chat(ctx, *, user_input=None):
    """Process user input and get response from AWS Bedrock"""
    if user_input is None:
        await ctx.send("Please provide a message after `!chat`. For example: `!chat Tell me a joke.`")
        return
        
    try:
        async with ctx.typing():
            
            payload = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "system": SYSTEM_PROMPT,
                "messages": [
                    {"role": "user", "content": user_input}
                ]
            }
            
            response = bedrock_runtime.invoke_model(
                modelId=BEDROCK_DEFAULT_MODELS,
                body=json.dumps(payload)
            )
            
            response_body = json.loads(response.get("body").read())
            
            if "completion" in response_body:
                ai_response = response_body.get("completion")
            elif "content" in response_body:
                ai_response = response_body.get("content")[0].get("text")
            else:
                ai_response = str(response_body) 
            
            await ctx.send(ai_response)
    
    except Exception as e:
        await ctx.send(f"Error processing your request: {str(e)}")
        print(f"Error: {str(e)}")

@chat.error
async def chat_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide a message after `!chat`. For example: `!chat Tell me a joke.`")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

def main():
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()