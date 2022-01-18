import os
import discord
from dotenv import load_dotenv

from clients.billy import Billy

def main():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    #GUILD = os.getenv('DISCORD_GUILD')

    bot = Billy(
        command_prefix="$",
        description='Robot Billy'
    )

    bot.load_extension("cogs.voicechannelcog")
    bot.load_extension("cogs.admincog")
    bot.load_extension("cogs.minecraftcog")
    bot.run(TOKEN, bot=True)

if __name__ == '__main__':
    main()
