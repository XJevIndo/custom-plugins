import datetime
import asyncio
import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel


class Training(commands.Cog):
    """Training Announcement System"""

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.command(aliases=["tchannel"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def trainingchannel(self, ctx, channel: discord.TextChannel):
        """Set the training channel!"""
        await self.db.find_one_and_update({"_id": "config"}, {"$set": {"training_channel": channel.id}}, upsert=True)

        embed = discord.Embed(color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Set Channel", value=f"Successfully set the training channel to {channel.mention}",
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=["tmention"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def trainingmention(self, ctx, *, mention: str):
        """Sets the training mention"""
        await self.db.find_one_and_update({"_id": "config"}, {"$set": {"training_mention": mention}}, upsert=True)

        embed = discord.Embed(color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Changed Mention", value=f"Successfully changed the training mention to {mention}",
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=["train"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def training(self, ctx):
        """Host a training."""
        try:
            config = await self.db.find_one({"_id": "config"})
            training_channel = config["training_channel"]
            setchannel = discord.utils.get(ctx.guild.channels, id=int(training_channel))

            try:
                training_mention = config["training_mention"]
            except KeyError:
                training_mention = ""

            embed = discord.Embed(
                description="Salutations, a training is currently being hosted at the Training Center! Come to the "
                            "Training Center for a chance of a promotion!",
                timestamp=datetime.datetime.utcnow())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            embed.color = self.bot.main_color
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/icons/1012278060499865610/fa261db6bfb06e127b63c0865cd9c6ca.webp")
            embed.set_footer(text="Latte Corporation")

            embed.add_field(name="Host:",
                            value=f"{ctx.author.mention} | {ctx.author.name}#{ctx.author.discriminator} | {ctx.author.nick}",
                            inline=False)
            embed.add_field(name="Training Center Link:", value=f"Click [here](https://www.roblox.com/games/7982194070/Training-Center-Latte-In-Dev).",
                            inline=False)
            msggg = await setchannel.send(training_mention, embed=embed)
            await asyncio.sleep(5)
            await msggg.edit(content=f"{training_mention} | msgID: {msggg.id}", embed=embed)
            await ctx.send(
                "<a:check:1012278060499865610> | Training announcement has been posted!")
        except discord.ext.commands.CommandOnCooldown:
            print("cooldown")

    @commands.command(aliases=["et"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def endtraining(self, ctx, *, msgID: str):
        """End a training."""
        config = await self.db.find_one({"_id": "config"})
        channel = self.bot.get_channel(config["training_channel"])
        try:
            training_mention = config["training_mention"]
        except KeyError:
            training_mention = ""
        try:
            msgID: int(msgID)
            message = await channel.fetch_message(msgID)
        except:
            embed = discord.Embed(title="Please include a valid Message ID that is in the training channel.",
                                  description="[Where can I find a Message ID?]("
                                              "https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)",
                                  color=0xe74c3c)
            await ctx.send(embed=embed)
        embed2 = discord.Embed(title="Latte Cafe",
                               description=f"The training by **{ctx.author.mention} | {ctx.author.name}#{ctx.author.discriminator}** has concluded! You can see our Trello to see our Training Schedule or See Training Center description.",
                               color=0xe74c3c)
        embed2.set_thumbnail(
            url="https://cdn.discordapp.com/icons/1012278060499865610/fa261db6bfb06e127b63c0865cd9c6ca.webp")
        embed2.set_footer(text="Latte Corporation")
        await message.edit(embed=embed2, content=training_mention)  # <@&695243187043696650>

        await ctx.send(
            "<a:check:1012278060499865610> | Training announcement has been edited and the training has ended!")
        await asyncio.sleep(1200)
        await message.delete()


async def setup(bot):
    await bot.add_cog(Training(bot))
