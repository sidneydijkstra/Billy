import os
import discord
from dotenv import load_dotenv
load_dotenv()

from clients.billycontroller import BillyController

if __name__ == '__main__':
    BillyController.setup()
