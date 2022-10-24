import datetime
import asyncio
import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel


class Shift(commands.Cog):
    """Shift Announcement System"""

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)

    @commands.command(aliases=["schannel"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def shiftchannel(self, ctx, channel: discord.TextChannel):
        """Set the shift channel!"""
        await self.db.find_one_and_update({"_id": "config"}, {"$set": {"shift_channel": channel.id}}, upsert=True)

        embed = discord.Embed(color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Set Channel", value=f"Successfully set the shift channel to {channel.mention}",
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=["smention"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def shiftmention(self, ctx, *, mention: str):
        """Sets the shift mention"""
        await self.db.find_one_and_update({"_id": "config"}, {"$set": {"shift_mention": mention}}, upsert=True)

        embed = discord.Embed(color=discord.Color.blue(), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Changed Mention", value=f"Successfully changed the shift mention to {mention}",
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=["s"])
    @checks.has_permissions(PermissionLevel.OWNER)
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def shift(self, ctx):
        """Host a shift."""
        try:
            config = await self.db.find_one({"_id": "config"})
            shift_channel = config["shift_channel"]
            setchannel = discord.utils.get(ctx.guild.channels, id=int(shift_channel))

            try:
                shift_mention = config["shift_mention"]
            except KeyError:
                shift_mention = ""

            embed = discord.Embed(
                description="Salutations, a shift is currently being hosted at the Cafe! Head down to Cafe and get our signature Coffee!",
                timestamp=datetime.datetime.utcnow())
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar)
            embed.color = self.bot.main_color
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/icons/1012278060499865610/fa261db6bfb06e127b63c0865cd9c6ca.webp")
            embed.set_footer(text="Latte Corporation")

            embed.add_field(name="Host:",
                            value=f"{ctx.author.mention} | {ctx.author.name}#{ctx.author.discriminator} | {ctx.author.nick}",
                            inline=False)
            started_at = datetime.datetime.utcnow()
            timestamp = round(datetime.datetime.timestamp(started_at))
            timestamp_show = f"<t:{timestamp}:R>"
            embed.add_field(name="Session Status:", value=f"Started {timestamp_show}", inline=False)
            embed.add_field(name="Cafe Link:",
                            value=f"Click [here](https://www.roblox.com/games/7652681872/Latt-Caf-In-Dev).",
                            inline=False)

            msggg = await setchannel.send(shift_mention, embed=embed)
            await asyncio.sleep(5)
            await msggg.edit(content=f"{shift_mention} | msgID: {msggg.id}", embed=embed)
            await ctx.send(
                "<a:check:742680789262663710> | Shift announcement has been posted!")
        except discord.ext.commands.CommandOnCooldown:
            print("cooldown")

    @commands.command(aliases=["es"])
    @checks.has_permissions(PermissionLevel.OWNER)
    async def endshift(self, ctx, *, msgID: str):
        """End a shift."""
        config = await self.db.find_one({"_id": "config"})
        channel = self.bot.get_channel(config["shift_channel"])
        try:
            shift_mention = config["shift_mention"]
        except KeyError:
            shift_mention = ""
        try:
            msgID: int(msgID)
            message = await channel.fetch_message(msgID)
        except:
            embed = discord.Embed(title="Please include a valid Message ID that is in the shift channel.",
                                  description="[Where can I find a Message ID?]("
                                              "https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)",
                                  color=0xe74c3c)
            await ctx.send(embed=embed)
        embed2 = discord.Embed(title="Latte Cafe Shifts",
                               description=f"The shift by **{ctx.author.mention} | {ctx.author.name}#{ctx.author.discriminator}** has ended! You can always attend next shift.",
                               color=0xe74c3c)
        embed2.set_thumbnail(
            url="https://cdn.discordapp.com/icons/1012278060499865610/fa261db6bfb06e127b63c0865cd9c6ca.webp")
        embed2.set_footer(text="Latte Corporation")
        await message.edit(embed=embed2, content=shift_mention)  # <@&695243187043696650>
        await ctx.send("<a:check:742680789262663710> | Thanks for Hosting a Shift! Now your shift has ended! Message will be deleted soon.")
        await asyncio.sleep(1200)
        await message.delete()


async def setup(bot):
    await bot.add_cog(Shift(bot))
