import discord
from discord.ext import commands 
import subprocess

class SBPHRclone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='purgegd')
    @commands.has_role("Dev and Maintainer")
    async def purge_gd(self, ctx):
        """
        Purges and cleans Google Drive where bot uploads reside. Only Admin/Dev can use this command.
        """
        try:
            await ctx.message.add_reaction('🕒')
            proc = subprocess.Popen(['rclone', 'delete', 'gd:', '--drive-use-trash=false', '-vv'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logs = ''
            while proc.poll() is None:
                line = proc.stdout.readline().decode()
                if line != '':
                    print(line.rstrip())
                    logs += line
            stdout, stderr = proc.communicate()
            print(stdout.decode())
            print(stderr.decode())
            logs += stdout.decode() + stderr.decode()
            custom_message = "=================================================================================\nLOGS FOR SBPH GOOGLE DRIVE, CHECK LINES BELOW ON WHAT THIS COMMAND DELETED!\n=================================================================================\n"
            with open('/home/xceon/network-share/houshou-py/rclone_logs.txt', 'w') as f:
                f.write(custom_message + logs)
            await ctx.message.add_reaction('✅')
            await ctx.reply('<@804650950026330172> storage contents nuked successfully.\nRClone logs attached below.', file=discord.File('/home/xceon/network-share/houshou-py/rclone_logs.txt'))
        except subprocess.CalledProcessError as e:
            await ctx.message.add_reaction('❌')
            await ctx.reply(f'Failed to nuke storage, reason: {e}')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.reply("You do not have permission to use this command. Ping **Dev and Maintainer** role or send **Aspidiske.** a message in <#1081849979854917633> if you think the bot storage is full!")
        else:
            raise error

def setup(bot):
    bot.add_cog(SBPHRclone(bot))
