import discord
import logging

from discord.ext import commands
from helpers import *
from exceptions import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Env(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.env_agents = {}
        for env in get_supported_envs():
            self.env_agents[env] = None

    @commands.group()
    async def env(self, ctx):
        self.guild = ctx.guild
        self.gid = ctx.guild.id

        if ctx.invoked_subcommand is None:
            await ctx.send("Εν ξέρω έτσι πράμα. Use !help")
    
    @env.command()
    async def describe(self, ctx, *params):
        try:
            if len(list(params)) == 0: raise EnvironmentNameNotProvidedException
            env_name = list(params)[0].lower()
            if not is_env_supported(env_name): raise EnvironmentNotSupportedException
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
        except EnvironmentNameNotProvidedException:
            await ctx.channel.send("Δώσμου όνομα. Environment name not provided.")
        except EnvironmentNotSupportedException:
            await ctx.channel.send("Ένεκαμα τρέιν τζαμέ κόμα.  Try another environemnt or use !help!")

    @env.command()
    async def train(self, ctx, *params):
        try:
            if len(list(params)) == 0: raise EnvironmentNameNotProvidedException
            env_name = list(params)[0].lower()
            if not is_env_supported(env_name): raise EnvironmentIsNotSupportedException
            gym_name = get_gym_name(env_name)
            
            if self.env_agents[gym_name] is not None: raise AgentAlreadyExistsException
            
            agent = Agent(gym_name)
            self.env_agents[gym_name] = agent
            
            await agent.train()
            env_role = await self.guild.create_role(name="Agent-" + gym_name, mentionable=True)
            await ctx.message.author.add_roles(env_role)
            overwrites = {
                # Everyone
                self.guild.get_role(self.gid): discord.PermissionOverwrite(read_messages=False),
                self.bot.user: discord.PermissionOverwrite(read_messages=True),
                env_role: discord.PermissionOverwrite(read_messages=True)
            }
            category = await self.guild.create_category(name=env_name, overwrites=overwrites)
            testing_channel = await self.guild.create_text_channel(name=gym_name, category=category)
            await testing_channel.send("Κοπέλια έμαθα τα ούλλα.")
        except EnvironmentNameNotProvidedException:
            await ctx.channel.send("Δώσμου όνομα. Environment name not provided.")
        except EnvironmentIsNotSupportedException:
            await ctx.channel.send("Έντο ξέρω τούτο.  Try another environemnt or use !help!")
        except AgentAlreadyExistsException:
            await ctx.channel.send("Ρε κουμπάρε μόλις τωρά ετέλιοσα! Άησμε να πνάσω. Try another environemnt or use !help!")

    @env.command()
    async def test(self, ctx, *params):
        try:
            if ctx.channel.category.name not in ctx.channel.name: raise NotInCorrectCategoryChannelException
            if len(list(params)) == 0: raise EnvironmentNameNotProvided
            env_name = list(params)[0].lower()
            if not is_env_supported(env_name): raise EnvironmentIsNotSupportedException
            gym_name = get_gym_name(env_name)
            
            agent = self.env_agents[gym_name]
            agent.test()
        except NotInCorrectCategoryChannelException:
            await ctx.channel.send("Πρέπει να είσαι channel του category. You have to be in the channel's category!")
        except EnvironmentNameNotProvided:
            await ctx.channel.send("Δώσμου όνομα. Environment name not provided.")
        except EnvironmentIsNotSupportedException:
            await ctx.channel.send("Έντο ξέρω τούτο.  Try another environemnt or use !help!")
        
    
    @env.command()
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    async def delete(self, ctx):
        try:
            if ctx.channel.category.name not in ctx.channel.name: raise NotInCorrectCategoryChannelException
            if len(ctx.channel.category.channels) == 1:
                env_role = discord.utils.get(self.guild.roles, name="Agent-" + ctx.channel.name)
                if env_role is not None:
                    await env_role.delete()
                category = ctx.channel.category
                await ctx.channel.delete()
                await category.delete()
                self.env_agents[ctx.channel.name] = None
            else:
                await ctx.channel.delete()
        except NotInCorrectCategoryChannelException:
            await ctx.channel.send("Πρέπει να είσαι σε channel του category. You have to be in the channel's category!")

def setup(bot):
    bot.add_cog(Env(bot))