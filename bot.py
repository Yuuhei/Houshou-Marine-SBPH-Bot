import json
import os
import platform
from colorama import Fore, Back, Style
import random
from random import randint
import sys
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

"""	
Setup bot intents (events restrictions)
For more information about intents, please go to the following websites:
https://discordpy.readthedocs.io/en/latest/intents.html
https://discordpy.readthedocs.io/en/latest/intents.html#privileged-intents


Default Intents:
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.emojis = True
intents.bans = True
intents.guild_typing = False
intents.typing = False
intents.dm_messages = False
intents.dm_reactions = False
intents.dm_typing = False
intents.guild_messages = True
intents.guild_reactions = True
intents.integrations = True
intents.invites = True
intents.voice_states = False
intents.webhooks = False

Privileged Intents (Needs to be enabled on dev page), please use them only if you need them:
intents.presences = True
intents.members = True
"""

intents = discord.Intents.default()

bot = Bot(command_prefix=config["bot_prefix"], intents=intents)  

@bot.event
async def on_ready():
    print(Fore.MAGENTA + f"Ahoy, {bot.user.name} here! Script loaded and ready to sail!")
    print(Fore.RED + "-------------------")
    print(Fore.GREEN + f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print(Fore.RED + "-------------------")
    print(Style.RESET_ALL)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="I'm broke | h!help"))

bot.remove_command("help")

if __name__ == "__main__":
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return
    with open("blacklist.json") as file:
        blacklist = json.load(file)
    if message.author.id in blacklist["ids"]:
        return
    await bot.process_commands(message)

@bot.event
async def on_command_completion(ctx):
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    print(
        Fore.YELLOW + f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})")
    print(Style.RESET_ALL)

    botwebhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/1021787265451696220/NfNabJvLiM25HzmzCyS0oMaca-n6piTHtF7kCkchzJ7F3sxL3rXN8ZspsCcyuD5mgIB0', rate_limit_retry=True,)
    timenow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    embed = DiscordEmbed(title=f'Bot Action Log', description=f"✅ Executed `{executedCommand}` command by <@{ctx.message.author.id}> at `{timenow} UTC -8`", color='bf40bf')
    embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/804650950026330172/ed49e0e623675c87c90ccbae537b7ffa.png')
    embed.set_footer(text="I'm just logging script activities for easier troubleshooting, do i look creepy?")
    botwebhook.add_embed(embed)
    botwebhook.execute()

@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Hey, please slow down! You're stressing me out!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="You are missing the permission `" + ", ".join(
                error.missing_perms) + "` to execute this command!",
            color=0xE02B2B
        )
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Wait a minute...",
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        embed.set_footer(text=f"Trying to use Qobuz? Refer to #music-dl-faq channel for audio quality/format selection.")
        await context.reply(embed=embed)
    elif isinstance(error, commands.MaxConcurrencyReached):
        embed = discord.Embed(
            title="Whoops! Not too fast!",
            description="Please wait for the previous downloads to finish!\nTry Again later.",
            color=0xE02B2B
        )
        embed.set_footer(text=f"Requested by {context.message.author}.")
        await context.send(embed=embed)     
    elif isinstance(error, commands.MissingAnyRole):
        embed = discord.Embed(
            title="Sorry!",
            description="Only donators can use this command! Refer to <#1079251617926365306> channel for more info!",
            color=0xE02B2B
        )
        embed.set_footer(text=f"Running this bot on my home's local machine 24/7, help me pay my electric bills please UwU")
        await context.send(embed=embed)
    raise error

bot.run(config["token"])
