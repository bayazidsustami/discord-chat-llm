import discord

def register_utility_commands(bot, model_handler):
    @bot.command(name="ping", help="Check if the bot is online")
    async def ping(ctx):
        await ctx.reply("Pong! 🏓")
    
    @bot.command(name="help", help="Show this help message")
    async def help_command(ctx):
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
            name="/image-styles",
            value="Show available image styles.",
            inline=False
        )
        
        embed.add_field(
            name="/about",
            value="Show information about this bot.",
            inline=False
        )

        embed.add_field(
            name="/fact",
            value="Get a random Garfield fact.",
            inline=False
        )
        embed.add_field(
            name="/quote",
            value="Get a random Garfield quote.",
            inline=False
        )
        embed.add_field(
            name="/lasagna",
            value="Get a lasagna recipe.",
            inline=False
        )
        embed.add_field(
            name="/joke",
            value="Get a Garfield-style joke.",
            inline=False
        )
        embed.add_field(
            name="/monday",
            value="Express Garfield's feelings about Mondays.",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @bot.command(name="about", help="Show information about this bot")
    async def about(ctx):
        embed = discord.Embed(
            title="About Discord LLM Bot",
            description="I'm a Discord bot that uses AWS Bedrock to provide AI-powered chat and image generation capabilities.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="Features",
            value="• AI chat responses when mentioned\n• Direct message chat support\n• Image generation with various styles",
            inline=False
        )
        
        embed.add_field(
            name="Usage",
            value="• Chat with me by mentioning me in a channel\n• Send me direct messages\n• Use `/image <prompt>` or `/image <image-style>:<prompt>` to generate images\n• Use `/help` to see all commands",
            inline=False
        )
        
        embed.set_footer(text="Powered by AWS Bedrock")
        
        await ctx.send(embed=embed)
