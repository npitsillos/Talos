import discord
import logging

from discord.ext import commands
from utils import *
from exceptions import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Env(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def env(self, ctx):
        self.guild = ctx.guild
        self.gid = ctx.guild.id
        
        if ctx.invoked_subcommand is None:
            await ctx.send("Εν ξέρω έτσι πράμα. Use !help")
    
    @env.command()
    async def describe(self, ctx, *params):
        env_name = list(params)[0].lower()
        if env_name not in SUPPORTED_ENVS: raise EnvironmentIsNotSupportedException
        env_dict = get_env_details(env_name)
        gym_name = list(env_dict.keys())[0]
        embed = discord.Embed(
            title=gym_name,
            description="Observation Space: {}\nAction Space: {}".format(env_dict[gym_name]["obs_space"], env_dict[gym_name]["action_space"]),
            colour=discord.Colour.blue()
        )
        await ctx.send(embed=embed)