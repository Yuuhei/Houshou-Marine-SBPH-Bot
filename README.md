![alt text](https://github.com/Yuuhei/Houshou-Marine-SBPH-Bot/blob/main/marine-banner.gif?raw=true)

# Houshou Marine SBPH Bot
A bot for SBPH coded by Aspidiske/Yuuhei and thepanglossian

You must use any Linux distro here, Windows isn't a linux distro.

If ur gonna plan to use another [OS](https://templeos.org/), you'll gonna have a bad time porting commands.

## Package Dependencies

Install the following packages before proceeding.

```sudo apt install python3 pip libjpeg-dev zlib1g-dev python3-dev libffi-dev libxml2-dev libxslt-dev```
then add Python to your path.

Run these to install additional important stuff: 

```pip3 install streamrip --upgrade```

```pip install -U discord.py```

Install [RClone](https://rclone.org/)

Install ```7zip``` or ``p7zip``

 Run ```pip install -r requirements.txt```

## Setting Up 

Run ```rip config --open``` , it will show you the file location of streamrip's config. Open it with a text editor and change

```folder = "/home/<user>/StreamripDownloads"``` to ```folder = "Your bot folder/download/Temp/"```

Set ```[database]
enabled = true``` to **false**.

Read [this](https://rclone.org/commands/rclone_config/) to setup rclone.

Change rclone remote to your rclone remote name on cogs/*.py from `rclone_drives = ["gd", "gd", "gd"]` to your remote name.

Open the config.json file and edit it.
* config.json download location should have a ```/``` at the end.

* Put the channel id in 6 and 7 of config.json

## About KHInsider Downloader

If khi_dl_arm binary isnt present in resources folder, download it on [this](https://github.com/Sorrow446/KHInsider-Downloader) repository

## All set?
If all set, run:

```python3 bot.py```

* When you run the h!dl <link> command for the first time , check your terminal and follow the steps to login to tidal/qobuz.

Your token is saved so you don't have to do it everytime.
