import discord
from discord.ext import commands

class CustomHelpCommand(commands.HelpCommand):
    
    def __init__(self):
        super().__init__(
            command_attrs={
                'help': 'Shows help about the bot, a command, or a category',
                'cooldown': commands.CooldownMapping.from_cooldown(1, 3.0, commands.BucketType.member)
            }
        )
        self.embed_color = discord.Color.blue()
    
    def get_command_signature(self, command):
        return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"
    
    def get_opening_note(self):
        return "Welcome to the Discord LLM Bot help system!"
    
    async def send_bot_help(self, mapping):
        embed = discord.Embed(
            title="Discord LLM Bot Help",
            description=self.get_opening_note(),
            color=self.embed_color
        )
        
        embed.add_field(
            name="Main Features",
            value=(
                "• AI chat responses when mentioned\n"
                "• Direct message chat support\n"
                "• Image generation with various styles\n"
                "• Multiple AI model support"
            ),
            inline=False
        )
        
        for cog, cmds in mapping.items():
            filtered = await self.filter_commands(cmds, sort=True)
            if filtered:
                cog_name = getattr(cog, "qualified_name", "Commands")
                if not filtered:
                    continue
                    
                commands_text = []
                for cmd in filtered:
                    brief = cmd.brief or cmd.help
                    if brief:
                        desc = brief.split('\n')[0] 
                        commands_text.append(f"`{cmd.name}` - {desc}")
                    else:
                        commands_text.append(f"`{cmd.name}`")
                
                value = "\n".join(commands_text)
                if value:
                    embed.add_field(
                        name=cog_name,
                        value=value,
                        inline=False
                    )
                
        embed.set_footer(text=f"Type {self.context.clean_prefix}help <command> for more details on a command.")
        
        channel = self.get_destination()
        await channel.send(embed=embed)
    
    async def send_command_help(self, command):
        """Send help for a specific command."""
        embed = discord.Embed(
            title=f"Command: {command.qualified_name}",
            description=command.help or "No detailed help available for this command.",
            color=self.embed_color
        )
        
        embed.add_field(
            name="Usage",
            value=f"`{self.get_command_signature(command)}`",
            inline=False
        )
        
        if command.aliases:
            embed.add_field(
                name="Aliases",
                value=", ".join(f"`{alias}`" for alias in command.aliases),
                inline=False
            )
        
        channel = self.get_destination()
        await channel.send(embed=embed)
    
    async def send_group_help(self, group):
        embed = discord.Embed(
            title=f"Command Group: {group.qualified_name}",
            description=group.help or "No detailed help available for this group.",
            color=self.embed_color
        )
        
        embed.add_field(
            name="Usage",
            value=f"`{self.get_command_signature(group)}`",
            inline=False
        )
        
        filtered = await self.filter_commands(group.commands, sort=True)
        if filtered:
            subcommands = []
            for cmd in filtered:
                subcommands.append(f"`{cmd.name}` - {cmd.short_doc or 'No description available'}")
            
            embed.add_field(
                name="Subcommands",
                value="\n.join(subcommands)",
                inline=False
            )
            embed.set_footer(text=f"Type {self.context.clean_prefix}help {group.qualified_name} <command> for more info on a subcommand.")
        
        # Send the embed
        channel = self.get_destination()
        await channel.send(embed=embed)
    
    async def send_cog_help(self, cog):
        """Send help for a specific category (cog)."""
        embed = discord.Embed(
            title=f"Category: {cog.qualified_name}",
            description=cog.description or "No description available for this category.",
            color=self.embed_color
        )
        
        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        if filtered:
            commands_list = []
            for cmd in filtered:
                commands_list.append(f"`{cmd.name}` - {cmd.short_doc or 'No description available'}")
            
            embed.add_field(
                name="Commands",
                value="\n".join(commands_list),
                inline=False
            )
        
        channel = self.get_destination()
        await channel.send(embed=embed)

def setup_help_command(bot):
    bot.help_command = CustomHelpCommand()
    return bot
