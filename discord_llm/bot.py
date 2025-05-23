import discord
from discord.ext import commands
import boto3

from config.settings import (
    DISCORD_TOKEN,
    BEDROCK_ACCESS_KEY_ID,
    BEDROCK_SECRET_ACCESS_KEY,
    BEDROCK_REGION,
    BEDROCK_DEFAULT_MODELS
)

from discord_llm.models.model_handler import BedrockModelHandler
from discord_llm.commands import register_all_commands


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="/", 
    intents=intents, 
    help_command=None,
    description="A Discord bot that uses AWS Bedrock to respond to user messages."
)

bot.remove_command("help")

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name=BEDROCK_REGION,
    aws_access_key_id=BEDROCK_ACCESS_KEY_ID,
    aws_secret_access_key=BEDROCK_SECRET_ACCESS_KEY,
)

model_handler = BedrockModelHandler(bedrock_runtime)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

async def extract_message_content(message):
    """Extract message content without the bot mention"""
    content = message.content.replace(f'<@{bot.user.id}>', '').strip()
    content = content.replace(f'<@!{bot.user.id}>', '').strip()
    return content

async def process_ai_response(content, model_id=BEDROCK_DEFAULT_MODELS):
    """Process message with AWS Bedrock and get AI response"""
    return await model_handler.process_request(content, model_id)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith("/"):
        await bot.process_commands(message)
        return
    
    if isinstance(message.channel, discord.DMChannel):
        content = message.content.strip()
        
        if not content:
            await message.channel.send("How can I help you?")
            return
        
        try:
            async with message.channel.typing():
                ai_response = await process_ai_response(content)
                await message.channel.send(ai_response)
        except Exception as e:
            await message.channel.send(f"Error processing your request: {str(e)}")
            print(f"Error: {str(e)}")
    
    elif bot.user.mentioned_in(message) and not message.mention_everyone:
        content = await extract_message_content(message)
        
        if not content:
            await message.channel.send("How can I help you?")
            return
        
        try:
            async with message.channel.typing():
                ai_response = await process_ai_response(content)
                await message.channel.send(ai_response)
        
        except Exception as e:
            await message.channel.send(f"Error processing your request: {str(e)}")
    
    await bot.process_commands(message)

def main():
    register_all_commands(bot, model_handler, process_ai_response)
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()