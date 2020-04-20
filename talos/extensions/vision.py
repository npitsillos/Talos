import discord
import logging
import aiohttp
import io

from discord.ext import commands
from talos.dl_utils.vision.mask_rcnn import MaskRCNN
from talos.dl_utils.vision.visualise import add_detections_to_images
from talos.dl_utils.helpers import *
from talos.exceptions import NotInCorrectCategoryChannelException, ModelNotSupportedException, ModelAlreadyExistsException, TooManyImagesException, NoImagesAttachedInMessageException
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Vision(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.models_created = {}
        for model in get_supported_models():
            self.models_created[model] = None

    @commands.group()
    async def vision(self, ctx):
        """
            Group of commands to interact with DL models
        """
        self.guild = ctx.guild
        self.gid = ctx.guild.id
        
        if ctx.invoked_subcommand is None:
            await ctx.send("Εν ξέρω έτσι πράμα. Use !help")

    @vision.command()
    async def ls(self, ctx):
        """
            Lists supported models
        """
        await ctx.channel.send("Έλα ρε μπροο! " + ','.join(get_supported_models()))
    
    @vision.command()
    async def create(self, ctx, model_name):
        """
            Creates an instance of the specified model
        """
        model_name = model_name.lower()
        if not is_model_supported(model_name): raise ModelNotSupportedException
        
        if self.models_created[model_name] is not None: raise ModelAlreadyExistsException
        model_role = await self.guild.create_role(name="Model-" + model_name, mentionable=True)
        await ctx.message.author.add_roles(model_role)
        overwrites = {
            # Everyone
            self.guild.get_role(self.gid): discord.PermissionOverwrite(read_messages=False),
            self.bot.user: discord.PermissionOverwrite(read_messages=True),
            model_role: discord.PermissionOverwrite(read_messages=True)
        }
        self.models_created[model_name] = MaskRCNN()
        category = await self.guild.create_category(name=model_name, overwrites=overwrites)
        testing_channel = await self.guild.create_text_channel(name=model_name, category=category)
        
        await testing_channel.send("Upload an image with every day objects in channel.".format(model_name))
        await ctx.channel.send("Κάμε άπλοουντ εικόνα στο channel ({}) να δεις!!!".format(model_name))
    
    @create.error
    async def create_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send_help(ctx.command)
        if isinstance(error.original, ModelNotSupportedException):
            await ctx.channel.send("Εν καταλάβω...")
        elif isinstance(error.original, ModelAlreadyExistsException):
            await ctx.channel.send("Ήδη έκαμες το τούτο...")

    @vision.command()
    async def run(self, ctx):
        """
            Runs model against attached input
        """
        if ctx.message.channel.name not in get_supported_models(): raise NotInCorrectCategoryChannelException
        attachments = ctx.message.attachments
        if len(attachments) == 0: raise NoImagesAttachedInMessageException
        if len(attachments) > 2: raise TooManyImagesException
        
        images = []
        names = []
        for attachment in attachments:
            names.append(attachment.filename)
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as resp:
                    images.append(Image.open(io.BytesIO(await resp.read())).convert("RGB"))

        images, predictions = self.models_created[ctx.message.channel.name].predict(images)
        image_path_objects = add_detections_to_images(names, images, predictions)

        for key in image_path_objects.keys():
            image_file = discord.File(image_path_objects[key]["path"])
            await ctx.channel.send(file=image_file)
            await ctx.channel.send("Τούτα ήβρα! " + ','.join(obj for obj in image_path_objects[key]["objects"]))

    @run.error
    async def run_error(self, ctx, error):
        if isinstance(error.original, NotInCorrectCategoryChannelException):
            await ctx.channel.send("Πρέπει να είσαι channel του model. You have to be in the mode's category!")
        elif isinstance(error.original, NoImagesAttachedInMessageException):
            await ctx.channel.send("Εν μου έδωκες εικόνα! No image given.")
        elif isinstance(error.original, TooManyImagesException):
            await ctx.message.channel.send("Όπααα ρεεε! Σιγά σιγά. Too many imagess! Only 2.")

def setup(bot):
    bot.add_cog(Vision(bot))