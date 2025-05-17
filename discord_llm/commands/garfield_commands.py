def register_garfield_commands(bot, process_ai_response):
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
