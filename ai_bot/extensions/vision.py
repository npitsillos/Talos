import discord
import logging
import aiohttp
import io

from discord.ext import commands
from mask_rcnn import *
from helpers import *
from exceptions import *
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Vision(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def vision(self, ctx):
        self.guild = ctx.guild
        self.gid = ctx.guild.id
        
        if ctx.invoked_subcommand is None:
            await ctx.send("Εν ξέρω έτσι πράμα. Use !help")

    @vision.command()
    async def models(self, ctx):
        await ctx.channel.send("Έλα ρε μπροο! " + ','.join(get_supported_models()))
    
    @vision.command()
    async def create(self, ctx, *params):
        try:
            if len(list(params)) == 0: raise ModelNameNotProvidedException
            if not is_model_supported(list(params)[0].lower()): raise ModelNotSupportedException
            model = list(params)[0].lower()
            model_role = await self.guild.create_role(name="Model-" + model, mentionable=True)
            await ctx.message.author.add_roles(model_role)
            overwrites = {
                # Everyone
                self.guild.get_role(self.gid): discord.PermissionOverwrite(read_messages=False),
                self.bot.user: discord.PermissionOverwrite(read_messages=True),
                model_role: discord.PermissionOverwrite(read_messages=True)
            }
            category = await self.guild.create_category(name=model, overwrites=overwrites)
            testing_channel = await self.guild.create_text_channel(name=model, category=category)
            
            await testing_channel.send("Upload an image wih every day objects.")
            await ctx.channel.send("Κάμε άπλοουντ εικόνα στο channel ({}) να δεις!!!".format(model))
        except ModelNameNotProvidedException:
            await ctx.channel.send("Δώσμου όνομα. Environment name not provided.")
        except ModelNotSupportedException:
            await ctx.channel.send("Εν καταλάβω...")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            attachments = message.attachments
            if len(attachments) > 0 and message.channel.name not in get_supported_models(): raise NotInCorrectCategoryChannelException
            # check only 1
            if len(attachments) > 2: raise TooManyImagesException
            images = []
            for attachment in attachments:
                async with aiohttp.ClientSession() as session:
                    # or use a session you already have
                    async with session.get(attachment.url) as resp:
                        images.append(Image.open(io.BytesIO(await resp.read())))
                        # buffer is a file-like
            print(images)
        except NotInCorrectCategoryChannelException:
            await message.channel.send("Πρέπει να είσαι σε channel του model που έκαμες. You have to be in the channel's model you created!")
        except TooManyImagesException:
            await message.channel.send("Όπααα ρεεε! Σιγά σιγά. Too many imagess! Only 2.")
def setup(bot):
    bot.add_cog(Vision(bot))