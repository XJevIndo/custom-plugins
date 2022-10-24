import asyncio
import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel


class botPrivacy(commands.Cog):
    """
    The privacy policy of Latte Corporation
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["myprivacy"])
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def privacy(self, ctx):
        """Send the Privacy Policy of Latte Corporation"""
        embed = discord.Embed(
            title="Latte Corporation Privacy Policy"
        )
        embed.set_author(name=str(ctx.author), icon_url=str(ctx.author.avatar_url))
        embed.description = """
                Privacy Policy will come out soon!
            """
        embed.color = self.bot.main_color
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(botPrivacy(bot))
