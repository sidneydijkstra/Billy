
# Billy  
A Discord bot programmed in python using the [discord.py](https://discordpy.readthedocs.io/en/stable/) api!  

### Dependencies
For this bot to run you have to install the requirements.txt file with pip.  
```
pip install -r requirements.txt  
```

You also have to install [ffmpeg](https://ffmpeg.org/) and include its /bin content in the .env file.  
Installation for linux:  
```
sudo add-apt-repository ppa:mc3man/trusty-media  
sudo apt-get update  
sudo apt-get install ffmpeg  
sudo apt-get install frei0r-plugins  
```

### Variables
Once you have installed all the dependencies you can create/edit the .env file with thees parameters:  
```
DISCORD_TOKEN=token  
DISCORD_GUILD=Channel Name  
FFMPEG_LOCATION=C:\folder\location\ffmpeg\bin\ffmpeg.exe  
```
The DISCORD_TOKEN is generated from the discord [dashboard](https://discord.com/developers) and needed for the bot to connect to the api of discord. DISCORD_GUILD is the name of the channel you want the bot to connect to (if you have multiple channels). And FFMPEG_LOCATION is the location of the ffmpeg.exe file, needed for the voice channel features to work.
