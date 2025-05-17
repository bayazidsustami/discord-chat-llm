import discord
from discord.ext import commands
import boto3
import base64
import io
from config.settings import (
    DISCORD_TOKEN,
    BEDROCK_ACCESS_KEY_ID,
    BEDROCK_SECRET_ACCESS_KEY,
    BEDROCK_REGION,
    BEDROCK_DEFAULT_MODELS
)

from discord_llm.models.model_handler import BedrockModelHandler
from discord_llm.help import setup_help_command


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

@bot.command(name="image", help="Generate an image based on a prompt. Optional: prefix with style: (e.g. 'pixel-art: a house')")
async def image(ctx, *, prompt: str):
    try:
        async with ctx.typing():
            style = "photographic"

            if ":" in prompt:
                parts = prompt.split(":", 1)
                potential_style = parts[0].strip().lower()
                
                style_presets = [
                    "photographic", "digital-art", "anime", "cinematic", "comic-book",
                    "fantasy-art", "line-art", "analog-film", "neon-punk", "isometric",
                    "low-poly", "origami", "modeling-compound", "3d-model", "pixel-art"
                ]
                
                if potential_style in style_presets:
                    style = potential_style
                    prompt = parts[1].strip()

            response_body = await model_handler.process_image_request(prompt, style)

            if "artifacts" in response_body:
                image_data = base64.b64decode(response_body["artifacts"][0]["base64"])
                file = discord.File(io.BytesIO(image_data), filename="generated_image.png")

                await ctx.reply(f"Generated image : ", file=file)
            else:
                await ctx.reply(f"Failed to generate image. No image data returned.")

    except Exception as e:
        await ctx.reply(f"Error generating image: {str(e)}")

@bot.command(name="fact", help="Get a random Garfield fact")
async def fact(ctx):
    try:
        async with ctx.typing():
            prompt = "Generate a fun, interesting fact about Garfield the cat. Keep it brief and entertaining."
            ai_response = await process_ai_response(prompt)
            await ctx.reply(ai_response)
    except Exception as e:
        await ctx.reply(f"Error generating Garfield fact: {str(e)}")

@bot.command(name="quote", help="Get a random Garfield quote")
async def quote(ctx):
    try:
        async with ctx.typing():
            prompt = "Generate a funny, authentic-sounding quote that Garfield the cat would say. Make it short and witty."
            ai_response = await process_ai_response(prompt)
            await ctx.reply(ai_response)
    except Exception as e:
        await ctx.reply(f"Error generating Garfield quote: {str(e)}")

@bot.command(name="lasagna", help="Get a lasagna recipe")
async def lasagna(ctx):
    try:
        async with ctx.typing():
            prompt = "Generate a delicious lasagna recipe that Garfield would love. Include ingredients and brief preparation steps."
            ai_response = await process_ai_response(prompt)
            await ctx.reply(ai_response)
    except Exception as e:
        await ctx.reply(f"Error generating lasagna recipe: {str(e)}")

@bot.command(name="joke", help="Get a Garfield-style joke")
async def joke(ctx):
    try:
        async with ctx.typing():
            prompt = "Tell a funny joke in the style of Garfield comics. Keep it short and in Garfield's sarcastic tone."
            ai_response = await process_ai_response(prompt)
            await ctx.reply(ai_response)
    except Exception as e:
        await ctx.reply(f"Error generating Garfield joke: {str(e)}")

@bot.command(name="monday", help="Express Garfield's feelings about Mondays")
async def monday(ctx):
    try:
        async with ctx.typing():
            prompt = "Express Garfield's hatred for Mondays in his own words. Make it funny and dramatic."
            ai_response = await process_ai_response(prompt)
            await ctx.reply(ai_response)
    except Exception as e:
        await ctx.reply(f"Error generating Monday rant: {str(e)}")

@bot.command(name="ping", help="Check if the bot is online")
async def ping(ctx):
    await ctx.reply("Pong! 🏓")

@bot.command(name="help", help="Show this help message")
async def help_command(ctx):
    """Display help information for the bot"""
    embed = discord.Embed(
        title="Help - Discord LLM Bot",
        description="Here are the commands you can use:",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="/image <prompt>",
        value="Generate an image based on a prompt. Optional: prefix with style: (e.g. 'pixel-art: a house')",
        inline=False
    )
    
    embed.add_field(
        name="/models",
        value="List all available AI models that can be used.",
        inline=False
    )
    
    embed.add_field(
        name="/about",
        value="Show information about this bot.",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name="models", help="List all available AI models that can be used")
async def models(ctx):
    try:
        available_models = await model_handler.list_available_models()
        
        embed = discord.Embed(
            title="Available AI Models",
            description="Here are the models you can use:",
            color=discord.Color.blue()
        )
        
        for model in available_models:
            embed.add_field(name=model["name"], value=model["description"], inline=False)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error fetching models: {str(e)}")

@bot.command(name="about", help="Show information about this bot")
async def about(ctx):
    """Display information about the bot and its capabilities"""
    embed = discord.Embed(
        title="About Discord LLM Bot",
        description="I'm a Discord bot that uses AWS Bedrock to provide AI-powered chat and image generation capabilities.",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="Features",
        value="• AI chat responses when mentioned\n• Direct message chat support\n• Image generation\n• Multiple AI model support",
        inline=False
    )
    
    embed.add_field(
        name="Usage",
        value="• Chat with me by mentioning me in a channel\n• Send me direct messages\n• Use `!image` to generate images\n• Use `!help` to see all commands",
        inline=False
    )
    
    embed.set_footer(text="Powered by AWS Bedrock")
    
    await ctx.send(embed=embed)

def main():
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()