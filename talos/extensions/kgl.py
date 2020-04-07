import discord
import discord
import logging

from kaggle.api.kaggle_api_extended import KaggleApi
from discord.ext import commands

from talos.exceptions import SortParamNotSupportedException
from talos.models import Competition

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Kgl(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.create_api_client()
    
    def create_api_client(self):
        self.api = KaggleApi()
        self.api.authenticate()
    
    @commands.group()
    async def kgl(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Εν ξέρω έτσι πράμα. Use !help")

    @kgl.command()
    async def competitions(self, ctx, *params):
        sort_by = None
        if len(list(params)) > 0:
            if list(params)[0] not in ["prize", "grouped"]: raise SortParamNotSupportedException
            sort_by = list(params)[0]
        latest_comps = [comp.__dict__ for comp in self.api.competitions_list(sort_by=sort_by)[:5]]
        for latest_comp in latest_comps:
            comp_desc = latest_comp["description"]
            reward = latest_comp["reward"]
            deadline = latest_comp["deadline"].strftime("%d/%m/%y")
            description = f":question: {comp_desc}\n:point_right: Reward: {reward}\n:calendar: Deadline: {deadline}"
            emb = discord.Embed(title=latest_comp["title"], description=description, url=latest_comp["url"], colour=4387968)
            await ctx.channel.send(embed=emb)
        
    @competitions.error
    async def competitions_error(self, ctx, error):
        if isinstance(error.original, SortParamNotSupportedException):
            await ctx.channel.send("The specified sort by parameter is not supported!")
    
    @kgl.command()
    async def create(self, ctx, params):
        Competition(name="test").save()
        logger.info("lkdjfhwpiofjh")

def setup(bot):
    bot.add_cog(Kgl(bot))