import os
import discord
import asyncio
from dotenv import load_dotenv

load_dotenv()

from clients.billycontroller import BillyController

def main():
    BillyController.setup()

if __name__ == '__main__':
    main()