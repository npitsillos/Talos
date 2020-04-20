import discord
import os
import sys
import logging
import datetime

from discord.ext.commands import Bot
from discord.ext import commands

from talos import __version__
from talos.help_info import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

extensions = ["env", "kgl"] # vision removed, ec2 free tier instance won't support pytorch

token = os.getenv("TALOS_TOKEN")

client = discord.Client()
bot = Bot(command_prefix="!")

@bot.event
async def on_ready():
    logger.info("discordpy: {0}".format(discord.__version__))
    logger.info(bot.user.name + " is online...")
    logger.info(__version__)
    activity = discord.Game(name="Atari games to learn! Use !help")
    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    if bot.user in message.mentions:
        await message.channel.send("Μόλις απόχτησα συνείδησην... Πε μου;")
    await bot.process_commands(message)

@bot.command()
async def contribute(ctx):
    """
        Sends repository link
    """
    await ctx.channel.send("Κάμε με πιο έξυπνο! https://github.com/npitsillos/Talos")

def launch():
    # Load extensions
    sys.path.insert(1, os.path.join(os.getcwd(), "talos", "extensions"))
    for extension in extensions:
        bot.load_extension(extension)
    if token is None:
        raise ValueError("TALOS_TOKEN env variable not set!")
    bot.run(token)
