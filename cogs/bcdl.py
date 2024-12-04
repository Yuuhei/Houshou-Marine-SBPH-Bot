import json
import os
import random
import sys
import subprocess
from PIL import Image
import pyqrcode
import discord
from discord.ext import commands
import time
import base64
from datetime import timedelta
from time import gmtime, strftime
import hashlib

# Only if you want to use variables that are in the config.json file.
if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

download_folder = config['bot_folder']
request_channel = config['request_channel']
upload_channel = config['upload_channel']

class BCDL(commands.Cog, name="bcdl"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.command(name="bcdl")
    # Here is the bot command cooldown. Comment these 2 lines to disable. @commands.cooldown time format is in seconds.
    # @commands.max_concurrency(1, per=BucketType.guild, wait=False)
    # @commands.cooldown(1, 90.0, commands.BucketType.guild)
    # -----------------------------------------------------------------------------------------------------------------
    # @commands.has_any_role("Leecher")
    async def dl(self, ctx, link):
        """
        Downloads music from Bandcamp. Check #how-to-use-bots for instructions how to use this command.
        """

        req_channel = self.bot.get_channel(request_channel)
        up_channel = self.bot.get_channel(upload_channel)

        rclone_drives = ["gd", "gd", "gd"]
        random_rclone_drives = random.choice(rclone_drives)

        if ctx.channel.id == request_channel:
            if link.find("artist") != -1:
                await ctx.reply(f"{ctx.author.mention}, downloading **Bandcamp Artist Profile and Playlists** not allowed for now.")
            elif link.find("bandcamp") != -1:
                await ctx.send(f"{ctx.author.mention}, Bandcamp track downloads are disabled for now. There's a major bug on Bandcamp downloads that makes the bot crash when a user tries to download a unavailable track. Bandcamp downloads will be back soon 😉")
            elif link.find("playlist") != -1:
                await ctx.reply(f"{ctx.author.mention}, downloading **Bandcamp Artist Profile and Playlists** not allowed for now.")
            elif link.find("tidal") != -1:
                await ctx.reply(f"{ctx.author.mention}, for **Tidal, Deezer, SoundCloud and YouTube** downloads, please use the `h!dl <link here>` command.")
            elif link.find("soundcloud") != -1:
                await ctx.reply(f"{ctx.author.mention}, for **Tidal, Deezer, SoundCloud and YouTube** downloads, please use the `h!dl <link here>` command.")
            elif link.find("music.apple") != -1:
                await ctx.reply(f"{ctx.author.mention}, **Apple Music** is not supported for now..")
            elif link.find("deezer") != -1:
                await ctx.reply(f"{ctx.author.mention}, for **Tidal, Deezer, SoundCloud and YouTube** downloads, please use the `h!dl <link here>` command.")
            elif link.find("qobuz") != -1:
                await ctx.reply(f"{ctx.author.mention}, for **Tidal, Deezer, SoundCloud and YouTube** downloads, please use the `h!dl <link here>` command.")
            elif link.find("youtube") != -1:
                await ctx.reply(f"{ctx.author.mention}, for **Tidal, Deezer, SoundCloud and YouTube** downloads, please use the `h!dl <link here>` command.")
            elif link.find("m.youtube") != -1:
                await ctx.reply(f"{ctx.author.mention}, for **Tidal, Deezer, SoundCloud and YouTube** downloads, please use the `h!dl <link here>` command.")
            elif link.find("youtu.be") != -1:
                await ctx.reply(f"{ctx.author.mention}, for **Tidal, Deezer, SoundCloud and YouTube** downloads, please use the `h!dl <link here>` command.")
            elif link.find("spotify") != -1:
                await ctx.reply(f"{ctx.author.mention}, for **Spotify** downloads, please use `h!spotdl <link here>` command.")
            elif not link.find(".com") != -1:
                await ctx.reply(f"**Invalid** link, {ctx.author.mention}. Please check your link before sending here.")
            elif not link.find("https") != -1:
                await ctx.reply(f"Please add `https://` to your link, {ctx.author.mention}.")
            else:
                await req_channel.set_permissions(ctx.guild.default_role, send_messages=False)
                await ctx.message.add_reaction('✅')
                await ctx.reply(f"{ctx.author.mention}, please wait while your request is being downloaded. You will receive a ping in <#974568872835448842> with your download link once it's done.\nTo other requestors, this channel will be **unlocked after completing the request.**")            

                download_start_time = time.time()
                try:
                    await ctx.message.add_reaction('📁')
                    subprocess.run(["mkdir", f"{download_folder}download/Temp"])
                    with open('bandcamp-dl_log.txt', 'wb') as f:
                        await ctx.message.add_reaction('📥')
                        process = subprocess.Popen(["campdown", f'{link}'], cwd=f"{download_folder}download/Temp", stdout=subprocess.PIPE)
                        for line in iter(process.stdout.readline, b''):
                            sys.stdout.buffer.write(line)
                            f.write(line)

                    download_end_time = time.time() - download_start_time                        
                    download_time = timedelta(seconds=round(download_end_time))

                    search_path = f'{download_folder}download/Temp'
                    root, dirs, files = next(os.walk(search_path), ([],[],[]))
                    try:
                        folder_name = dirs[0]
                    except:
                        file_name = files[0]

                    zipping_start_time = time.time()        

                    time_format_file_name = strftime("%Y-%m-%d_%H%M%S", gmtime())
                    try:
                        zip_file = f"{folder_name}_{time_format_file_name}.zip"
                    except:
                        zip_file = f"{file_name}_{time_format_file_name}.zip"               

                    await ctx.message.add_reaction('📦')
                    subprocess.run(["7z", "a", "-mx0", "-tzip", f"{download_folder}download/Temp/{zip_file}", f'{download_folder}download/Temp/'])

                    zipping_end_time = time.time() - zipping_start_time        
                    zipping_time = timedelta(seconds=round(zipping_end_time))

                    upload_start_time = time.time()

                    await ctx.message.add_reaction('🔒')
                    sha256_hash = hashlib.sha256()
                    with open(f"{download_folder}download/Temp/{zip_file}", "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            sha256_hash.update(chunk)
                    checksum = sha256_hash.hexdigest().upper()

                    with open('upload_log.txt', 'wb') as f:
                        await ctx.message.add_reaction('📤')
                        process = subprocess.Popen(["rclone", "copy", f'{download_folder}download/Temp/{zip_file}', f"{random_rclone_drives}:", "--progress", "--transfers", "16", "--drive-chunk-size", "32M"], stdout=subprocess.PIPE)
                        for line in iter(process.stdout.readline, b''):
                            sys.stdout.buffer.write(line)
                            f.write(line)

                    upload_end_time = time.time() - upload_start_time                            
                    upload_time = timedelta(seconds=round(upload_end_time))

                    subprocess.run(["rm", "-rf", f'{download_folder}download/Temp'])              

                    all_done = discord.Embed(
                        name="Request complete",
                        description="**Request Complete.**\nHelp me pay my electric bills, if you find me useful! Check <#1079251617926365306> for details!",
                        color=0x20e84f
                    )                

                    link_process = subprocess.run(["rclone", "link", f"{random_rclone_drives}:"f'{zip_file}', "--retries", "15"], stdout=subprocess.PIPE, encoding='utf-8')
                    gdrive_link = link_process.stdout        
                    
                    # Uncomment lines below if you want to generate qr codes for every uploads
                    # -----------------------------------------------------------------------------------------------------------------
                    # subprocess.run(["mkdir", f"{download_folder}qr-codes/gen"])
                    # qrCodeGen = pyqrcode.QRCode(gdrive_link, error='H')
                    # qrCodeGen.png(f'{download_folder}qr-codes/gen/request_qr.png', scale=10)  
                    # im = Image.open(f'{download_folder}qr-codes/gen/request_qr.png')
                    # im = im.convert("RGBA")
                    # logo = Image.open(f'{download_folder}resources/sbph_logo.jpg')
                    # box = (233,233,333,333)
                    # im.crop(box)
                    # region = logo
                    # region = region.resize((box[2] - box[0], box[3] - box[1]))
                    # im.paste(region,box)
                    # im.save(f'{download_folder}qr-codes/gen/request_qr.png')
                    # -----------------------------------------------------------------------------------------------------------------

                    request_link = link
                    gdrive_b64 = base64.b64encode(bytes(gdrive_link, "utf-8")).decode()

                    all_done.add_field(name="Name", value=zip_file, inline=False)
                    all_done.add_field(name="Request Link", value=request_link, inline=False)
                    all_done.add_field(name="Download Link (Plain Text for easier copy below)", value=gdrive_b64, inline=False)
                    all_done.add_field(name="Download Time", value=download_time, inline=False)
                    all_done.add_field(name="Zip Time", value=zipping_time, inline=False)
                    all_done.add_field(name="Upload Time", value=upload_time, inline=False) 
                    all_done.add_field(name="SHA-256 Checksum", value=checksum, inline=False)     
                    all_done.set_footer(text=f"Requested by {ctx.message.author}\nHoushou Marine - a SoundBytes PH's music downloader") 

                    await up_channel.send(embed=all_done)
                    await up_channel.send(f"{ctx.author.mention}, decode the link below in <#1087346196626034759>.")
                    await up_channel.send(gdrive_b64)
                    await ctx.message.add_reaction('👍')
                    await req_channel.send("Request complete! Download link sent on <#974568872835448842>!\nWaiting for command...")

                    # Uncomment lines below if you want to send dm to author
                    # -----------------------------------------------------------------------------------------------------------------
                    # dm_link = discord.Embed(
                    #     name="Request Complete!",
                    #     description=f"**Request Done.**\nHelp me pay my electric bills, if you find me useful! Check [this channel](https://discordapp.com/channels/974566288900915220/974578168700755989) for details!\n \n**Name**\n{zip_file}\n \n**Request Link**\n{request_link}\n \nBelow is the download link for your request, encoded in Base64.\nCopy the code below and paste it on Base64 decoder sites like <https://www.base64decode.org/>.\n \nAlternatively, you can scan the QR Code provided below for the direct Google Drive link.",
                    #     color=0x20e840
                    # )
                    # await ctx.author.send(embed=dm_link)
                    # await ctx.author.send(f"{gdrive_b64}")
                    # # send qr code via dm to author
                    # await ctx.author.send(file=discord.File(f'{download_folder}qr-codes/gen/request_qr.png'))
                    # time.sleep(1)
                    # subprocess.run(["rm", "-rf", f'{download_folder}qr-codes/gen'])    
                    # # await up_channel.send(f"{ctx.author.mention}")
                    await req_channel.set_permissions(ctx.guild.default_role, send_messages=True)
                    # await ctx.send("Done.")
                    # # await up_channel(config["request_channel"]).send("Channel unlocked, awaiting command.")
                    # -----------------------------------------------------------------------------------------------------------------
                except:
                    await ctx.message.add_reaction('❌')
                    await ctx.send("The following Song/Album isn't available to download. Possible reasons are:\n- Song/Album is geo-locked.\n- Bot cannot fetch link data, try again.")
                    await req_channel.set_permissions(ctx.guild.default_role, send_messages=True)

        else:
            await ctx.reply(f"This command can only be used in <#{request_channel}>")                                         
        
def setup(bot):
    bot.add_cog(BCDL(bot))
