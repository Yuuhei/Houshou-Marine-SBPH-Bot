import json
import os
import sys

import discord
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, context):
        """
        List all commands Houshou Marine supports.
        """
        prefix = config["bot_prefix"]
        if not isinstance(prefix, str):
            prefix = prefix[0]
        embed = discord.Embed(title="Help", description="Houshou Marine's available commands:", color=0x42F56C)
        for cog_name, cog in self.bot.cogs.items():
            if cog.get_commands():  # Check if cog has commands
                command_list = [command.name for command in cog.get_commands()]
                command_description = [command.help for command in cog.get_commands()]
                help_text = '\n'.join(f'{prefix}{n} - {h}' for n, h in zip(command_list, command_description))
                embed.add_field(name=cog_name.capitalize(), value=f'```{help_text}```', inline=False)
        await context.reply(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
