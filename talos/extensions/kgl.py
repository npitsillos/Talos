import discord
import discord
import logging

from kaggle.api.kaggle_api_extended import KaggleApi
from discord.ext import commands

class Kgl(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.create_api_client()
    
    def create_api_client(self):
        if hasattr(self, "api"):
            return
        else:
            self.api = KaggleApi()
            self.api.authenticate()
    
    @commands.group()
    async def kgl(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Εν ξέρω έτσι πράμα. Use !help")

    @kgl.command()
    async def competitions(self, ctx):
        # get only 5 latest comps
        for comp in self.api.competitions_list()[:5]:
            await ctx.channel.send(comp)

def setup(bot):
    bot.add_cog(Kgl(bot))