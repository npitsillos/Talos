import discord
import datetime
import logging

from kaggle.api.kaggle_api_extended import KaggleApi
from discord.ext import commands

from talos.exceptions import CategoryNotSupportedException, CompetitionNameNotProvidedException, CompetitionAlreadyExistsException
from talos.models import Competition
from talos.helpers import get_kaggle_comps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Kgl(commands.Cog):

    CATEGORIES = ["all", "featured", "research", "recruitment", "gettingStarted", "masters", "playground"]

    def __init__(self, bot):
        self.bot = bot
        self.create_api_client()
    
    def create_api_client(self):
        self.api = KaggleApi()
        self.api.authenticate()
    
    @commands.group()
    async def kgl(self, ctx):
        self.guild = ctx.guild
        self.gid = ctx.guild.id

        if ctx.invoked_subcommand is None:
            await ctx.send("Εν ξέρω έτσι πράμα. Use !help")

    @kgl.command()
    async def competitions(self, ctx, *params):
        category = self.CATEGORIES[0]
        if len(list(params)) > 0:
            if list(params)[0] not in self.CATEGORIES: raise CategoryNotSupportedException
            category = list(params)[0]
        comps = await get_kaggle_comps(self.api, category=category)
        latest_comps = [comp.__dict__ for comp in comps[:5]]
        for latest_comp in latest_comps:
            comp_desc = latest_comp["description"]
            reward = latest_comp["reward"]
            deadline = latest_comp["deadline"].strftime("%d/%m/%y")
            description = f":question: {comp_desc}\n:point_right: Reward: {reward}\n:calendar: Deadline: {deadline}"
            emb = discord.Embed(title=latest_comp["title"], description=description, url=latest_comp["url"], colour=4387968)
            await ctx.channel.send(embed=emb)
        
    @competitions.error
    async def competitions_error(self, ctx, error):
        if isinstance(error.original, CategoryNotSupportedException):
            await ctx.channel.send("The specified category is not supported!")
    
    @kgl.command()
    async def create(self, ctx, *params):
        if len(list(params)) == 0: raise CompetitionNameNotProvidedException
        # use first to find matching competition from Kaggle
        first_word = list(params)[0]
        comps = await get_kaggle_comps(self.api)
        latest_comps = [comp.__dict__ for comp in comps]
        matched_comps = []
        
        for i, latest_comp in enumerate(latest_comps):
            if first_word in latest_comp["title"].lower():
                matched_comps.append(latest_comp)
        
        if len(matched_comps) == 1:
            matched_comp = matched_comps[0]
            comp_cat_name = '-'.join(matched_comp["title"].split(' ')).lower()
            category = discord.utils.get(ctx.guild.categories, name=comp_cat_name)

            if category is not None:
                raise CompetitionAlreadyExistsException

            comp_role = await self.guild.create_role(name="Comp-" + comp_cat_name, mentionable=True)
            await ctx.message.author.add_roles(comp_role)
            overwrites = {
                # Everyone
                self.guild.get_role(self.gid): discord.PermissionOverwrite(read_messages=False),
                self.bot.user: discord.PermissionOverwrite(read_messages=True),
                comp_role: discord.PermissionOverwrite(read_messages=True)
            }
            category = await self.guild.create_category(name=comp_cat_name, overwrites=overwrites)
            general_channel = await self.guild.create_text_channel(name='general', category=category)
            
            logger.info(Competition(name=category, url=matched_comp["url"], created_at=datetime.datetime.now(), deadline=matched_comp["deadline"]).save())
            
            await general_channel.send("@here Άτε κοπέλια..!")
        elif len(matched_comps) > 1:
            await ctx.channel.send("Έσηει παραπάνω που ένα!")
            for matched_comp in matched_comps:
                comp_desc = matched_comp["description"]
                reward = matched_comp["reward"]
                deadline = matched_comp["deadline"].strftime("%d/%m/%y")
                description = f":question: {comp_desc}\n:point_right: Reward: {reward}\n:calendar: Deadline: {deadline}"
                emb = discord.Embed(title=matched_comp["title"], description=description, url=matched_comp["url"], colour=4387968)
                await ctx.channel.send(embed=emb)
        else:
            await ctx.channel.send("Νομίζω έφυε σου το όνομα! Use !kgl competitions to see a list.")
    
    @create.error
    async def create_error(self, ctx, error):
        if isinstance(error.original, CompetitionAlreadyExistsException):
            await ctx.channel.send("Ρεεεε τούτο το κομπετίσιον υπάρχει!!")
        elif isinstance(error.original, CompetitionNameNotProvidedException):
            await ctx.channel.send("Ε δώσμου όνομα ρε!!")

def setup(bot):
    bot.add_cog(Kgl(bot))