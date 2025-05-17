import base64
import io
import discord

style_presets = [
    "photographic", "digital-art", "anime", "cinematic", "comic-book",
    "fantasy-art", "line-art", "analog-film", "neon-punk", "isometric",
    "low-poly", "origami", "modeling-compound", "3d-model", "pixel-art"
]

def register_image_commands(bot, model_handler):
    @bot.command(name="image", help="Generate an image based on a prompt. Optional: prefix with style: (e.g. 'pixel-art: a house')")
    async def image(ctx, *, prompt: str):
        try:
            async with ctx.typing():
                style = "photographic"

                if ":" in prompt:
                    parts = prompt.split(":", 1)
                    potential_style = parts[0].strip().lower()
                    
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

    @bot.command(name="image-styles", help="Show available image styles.")
    async def image_styles(ctx):
        embed = discord.Embed(
            title="Available Image Styles",
            description="\n".join(f"- {style}" for style in style_presets),
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=embed)
