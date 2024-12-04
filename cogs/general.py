import json
import os
import platform
import sys
import discord
from discord.ext import commands
import subprocess

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

download_folder = config['bot_folder']
uname = platform.uname()

class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["botinfo"])
    async def info(self, context):
        """
        Get some useful (or not) information about Houshou Marine.
        """
        embed = discord.Embed(
            description="Houshou Marine - a SoundBytes PH's music downloader.",
            color=0x42F56C
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/804650950026330172/ed49e0e623675c87c90ccbae537b7ffa.png"
        )
        embed.set_author(
            name="❓ Bot Information"
        )
        embed.add_field(
            name="Bot Owner and Dev:",
            value="<@380793772088229888>",
            inline=True
        )
        embed.add_field(
            name="Helper:",
            value="thepanglossian#0091",
            inline=True
        )
        embed.add_field(
            name="Horni Team and Donators:",
            value="<@369686912568655875>, for providing Tidal Subs\n \n<@264355366551289856>, for providing the server (Dell Optiplex 3020M)\n \n<@305998511894167552>, for providing Unlimited Google Drive cloud storage\n \nAnd all <@&979375720432287775>s, thank you for donating!",
            inline=True
	)
        embed.add_field(
            name="Python Version:",
            value=f"{platform.python_version()}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"{config['bot_prefix']}",
            inline=False
        )
        embed.add_field(
            name="Running on:",
            value=f"Debian GNU/Linux 11 Headless {platform.system()} {platform.release()} ({os.name})",
            inline=False
        )
        embed.add_field(
            name="Server Specs:",
            value=f"Processor: Intel i3-4160T @ 3.10GHz, 2C/4T\nTotal Physical RAM: 6GB (4G+2G DDR3 SODIMM) @ 1333MHz\nStorage: 240GB SATA SSD",
            inline=False
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/899688146466385961/1034460067346530436/marine-banner.gif"
        )
        embed.set_footer(
            text=f"Requested by {context.message.author}"
        )
        await context.reply(embed=embed)

    @commands.command(name="ping")
    async def ping(self, context):
        """
        Check if the bot is alive and still sailing the pirate seas.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0x42F56C
        )
        await context.reply(embed=embed)

    @commands.command(name="invite", aliases=["support", "supportserver"])
    async def invite(self, context):
        """
        Get the invite link of SBPH Server.
        """
        embed = discord.Embed(
            description=f"Join the server for the bot by clicking these links:\n Vanity URL: https://discord.gg/soundbytesph\nNormal Invite Url (if vanity URL isn't working): https://discord.gg/mj2jbz3RWw",
            color=0xD75BF4
        )
        try:
            await context.author.send(embed=embed)
            await context.reply("I sent you a private message, pls respond")
        except discord.Forbidden:
            await context.reply(embed=embed)

    @commands.command(name="clean")
    @commands.has_any_role("Dev and Maintainer")
    async def clean(self, context):
        """
        Cleans temp folder of downloads, "usually" resolves Region Error. Only Admin/Dev can use this command!
        """
        subprocess.run(["rm", "-r", f"{download_folder}download/Temp"])
        embed = discord.Embed(
            title="👍 Success!",
            description=f"🗑️ Temp folder wiped.",
            color=0x42F56C
        )
        await context.reply(embed=embed)

def setup(bot):
    bot.add_cog(general(bot))
