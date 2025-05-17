from discord_llm.commands.image_commands import register_image_commands
from discord_llm.commands.utility_commands import register_utility_commands
from discord_llm.commands.garfield_commands import register_garfield_commands

def register_all_commands(bot, model_handler, process_ai_response):
    register_image_commands(bot, model_handler)
    register_utility_commands(bot, model_handler)
    register_garfield_commands(bot, process_ai_response)
    
