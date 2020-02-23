import discord
import os
import logging
import datetime

from discord.ext.commands import Bot
from discord.ext import commands

from help_info import *
from utils import *
from extensions import Env

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

token = os.getenv("TALOS_TOKEN")

client = discord.Client()
bot = Bot(command_prefix="!", help_command=None)

@bot.event
async def on_ready():
    logger.info(bot.user.name + " is online...")
    activity = discord.Game(name="Atari games to learn! Use !help")
    await bot.change_presence(activity=activity)

@bot.event
async def on_message(message):
    if bot.user in message.mentions:
        await message.channel.send("Μόλις απόχτησα συνείδησην... Πε μου;")
    await bot.process_commands(message)

async def send_help_page(ctx, page):
    help_info = "--- " + page.upper() + " HELP PAGE ---\n" + help_dict[page]
    while len(help_info) > 1900:  # Embed has a limit of 2048 chars
        idx = help_info.index('\n', 1900)
        emb = discord.Embed(description=help_info[:idx], colour=4387968)
        await ctx.author.send(embed=emb)
    emb = discord.Embed(description=help_info, colour=4387968)
    await ctx.author.send(embed=emb)

@bot.command()
async def help(ctx, *params):
    if isinstance(ctx.channel, discord.DMChannel):
        if len(params) > 0:
            for page in params:
                if page in help_dict.keys():
                    await send_help_page(ctx, page)
                else:
                    await ctx.channel.send("Έψαξα τα αρχεία μου αλλά ένηβρα έτσι πράμα. Τούτα είμαι χαρντκοουτετ να δείχνω: {}\n Artificial Intelligence μήσιημου...".format(" ".join(help_dict.keys())))
        else:
            for key in help_dict.keys():
                await send_help_page(ctx, key)
    else:
        await ctx.channel.send("Στείλε DM ρεεε να μεν μας θωρούν ούλλοι!")

@bot.command()
async def contribute(ctx):
    await ctx.channel.send("Κάμε με πιο έξυπνο! https://github.com/npitsillos/Talos")

@bot.command()
async def envs(ctx):
    await ctx.channel.send("Προτιμώ τα Atari αλλά τέλος πάντων... {}".format(" ".join(list(SUPPORTED_ENVS.keys()))))

def run_bot():
    bot.add_cog(Env(bot))
    bot.run(token)

if __name__ == "__main__":
    run_bot()