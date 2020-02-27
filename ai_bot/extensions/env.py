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
        if env_name not in SUPPORTED_ENVS.keys(): raise EnvironmentIsNotSupportedException
        env_dict = get_env_details(env_name)
        gym_name = env_dict["name"]
        description = "States: \n{} \
                        \n\n \
                        Observation Space: {}\n \
                        Action Space: {}".format("\n".join(["->".join(list(t)) for t in env_dict["states"].items()]), env_dict["obs_space"], env_dict["action_space"])
        embed = discord.Embed(
            title=gym_name,
            description=description,
            colour=discord.Colour.blue()
        )
        await ctx.send(embed=embed)

    @env.command()
    async def train(self, ctx, *params):
        env_name = list(params)[0].lower()
        if not check_supported_envs(env_name): raise EnvironmentIsNotSupportedException
        agent = Agent(env_name)
        await agent.train_agent()
        # await train_on_env(ctx, self.train_callback, params)
        await ctx.author.send("Eteliosaaa")
    