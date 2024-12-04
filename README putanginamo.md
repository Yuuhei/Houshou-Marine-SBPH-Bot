Houshou Marine bot.
A bot for SBPH coded by Meis Clauson and thepanglossian
You must use Debian or any Debian based linux distro to run this bot.
If ur gonna plan to use another OS, you'll gonna have a bad time porting commands.

## How to config
## Install the following packages before proceeding.

```sudo apt install python3 pip libjpeg-dev zlib1g-dev python3-dev libffi-dev libxml2-dev libxslt-dev```
then add Python to your path.

```pip3 install streamrip --upgrade```

```pip install -U discord.py```

```rclone```

```7zip```

```pip install -r requirements.txt```

## Setting up the bot is pretty straight forward.
Run ```rip config --open``` , it will show you the file location of streamrip's config. Open it with a text editor and change
```folder = "/Users/nathan/StreamripDownloads"``` to ```folder = "Your bot folder/download/Temp/"```

Set ```[database]
enabled = true``` to **false**.

Change rclone remote to your rclone remote name (Line 46)

Read <https://rclone.org/commands/rclone_config/> to setup rclone.

Open the config.json file and edit it.

config.json download location should have a ```/``` at the end.

Put the channel id in 6 and 7 of config.json

If khi_dl_arm binary isnt present in resources folder, download it here

https://github.com/Sorrow446/KHInsider-Downloader

## Run Bot
```python3 bot.py```

When you run the h!dl <link> command for the first time , check your terminal and follow the steps to login to tidal/qobuz.

Your token is saved so you don't have to do it everytime.
