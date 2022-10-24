import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import asyncio


class Reports(commands.Cog):
    """
    Easy report system right here!
    """

    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def report(self, ctx):
        """
        Report a player.
        """
        try:
            staffChannel = self.bot.get_channel(686253307278393442)
            guestChannel = self.bot.get_channel(686253328270884877)
            if ctx.guild.id == 814758983238942720:
                staffChannel = self.bot.get_channel(818446997816082432)
                guestChannel = self.bot.get_channel(818447055810199552)
             
            texta = """**React with the type of your report:**
  1️⃣ | Staff Report
  2️⃣ | Customer/Non-Staff Report
  ❌ | Cancel
  """

            embedTimeout = discord.Embed(description="❌ | You took too long! Command cancelled", color=15158332)
            embed1 = discord.Embed(description=texta, color=self.bot.main_color)
            embed1.set_footer(text="React with ❌ to cancel")
            reactionmsg = await ctx.send(content=f"<@!{ctx.author.id}>", embed=embed1)
            for emoji in ('1️⃣', '2️⃣', '❌'):
                await reactionmsg.add_reaction(emoji)

            def checkmsg(msg: discord.Message):
                return msg.channel == ctx.channel and msg.author == ctx.author

            def cancel_check(msg: discord.Message):
                return msg.content.lower() == "cancel" or msg.content.lower() == f"{ctx.prefix}cancel"

            def check(r, u):
                return u == ctx.author

            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=20.0, check=check)
            except asyncio.TimeoutError:
                return await reactionmsg.edit(embed=embedTimeout)

            if str(reaction.emoji) == '1️⃣':
                await reactionmsg.clear_reactions()

                text = "**Staff Report**\nWhat is the username of the user you're reporting? You have 5 minutes to " \
                       "reply.\n\n*Say 'cancel' to cancel the report.* "
                await reactionmsg.edit(embed=discord.Embed(description=text, color=self.bot.main_color))

                try:
                    username = await self.bot.wait_for('message', check=checkmsg, timeout=360)
                    if cancel_check(username) is True:
                        cancelEmbed = discord.Embed(description="❌ | Cancelled report", color=15158332)
                        await reactionmsg.edit(embed=cancelEmbed)
                        await reactionmsg.clear_reactions()
                        return
                except asyncio.TimeoutError:

                    return await reactionmsg.edit(embed=embedTimeout)
                await username.delete()

                text = "**Staff Report**\nWhat is the rank of the suspect? You have 5 minutes to reply.\n\n*Say " \
                       "'cancel' to cancel the report.* "
                await reactionmsg.edit(embed=discord.Embed(description=text, color=self.bot.main_color))

                try:
                    rank = await self.bot.wait_for('message', check=checkmsg, timeout=360)
                    if cancel_check(rank) is True:
                        cancelEmbed = discord.Embed(description="❌ | Cancelled report", color=15158332)
                        await reactionmsg.edit(embed=cancelEmbed)
                        await reactionmsg.clear_reactions()
                        return
                except asyncio.TimeoutError:
                    return await reactionmsg.edit(embed=embedTimeout)
                await rank.delete()

                text = "**Staff Report**\nWhat is the reason for this report? You have 5 minutes to reply.\n\n*Say " \
                       "'cancel' to cancel the report.* "
                await reactionmsg.edit(embed=discord.Embed(description=text, color=self.bot.main_color, ))

                try:
                    reason = await self.bot.wait_for('message', check=checkmsg, timeout=360)
                    if cancel_check(reason) is True:
                        cancelEmbed = discord.Embed(description="❌ | Cancelled report", color=15158332)
                        await reactionmsg.edit(embed=cancelEmbed)
                        await reactionmsg.clear_reactions()
                        return
                except asyncio.TimeoutError:
                    return await reactionmsg.edit(embed=embedTimeout)
                await reason.delete()

                text = "**Staff Report**\nPlease provide proof of this happening. You can upload a video/image or use " \
                       "a link to an image or video. The report will be sent right after. You have 10 minutes to " \
                       "reply.\n\n*Say 'cancel' to cancel the report.* "
                await reactionmsg.edit(embed=discord.Embed(description=text, color=self.bot.main_color))

                try:
                    proof = await self.bot.wait_for('message', check=checkmsg, timeout=600)
                    if cancel_check(proof) is True:
                        cancelEmbed = discord.Embed(description="❌ | Cancelled report", color=15158332)
                        await reactionmsg.edit(embed=cancelEmbed)
                        await reactionmsg.clear_reactions()
                        return
                except asyncio.TimeoutError:
                    return await reactionmsg.edit(embed=embedTimeout)
                my_files = [await x.to_file() for x in proof.attachments]
                await proof.delete()

                reportEmbed = discord.Embed(title="New Staff Report", color=self.bot.main_color)
                reportEmbed.add_field(name="Username:", value=username.content)
                reportEmbed.add_field(name="Rank:", value=rank.content)
                reportEmbed.add_field(name="Reason:", value=reason.content)
                if proof.content:
                    reportEmbed.add_field(name="Proof:", value=proof.content)
                reportEmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar)

                await staffChannel.send(content="---------------------------", embed=reportEmbed, files=my_files)
                text = "✅ | The report has successfully been sent!"
                await reactionmsg.edit(embed=discord.Embed(description=text, color=3066993))

            if str(reaction.emoji) == '2️⃣':
                await reactionmsg.clear_reactions()

                text = "**Customer/Non-Staff Report**\nWhat is the username of the user you're reporting? You have 5 minutes to " \
                       "reply.\n\n*Say 'cancel' to cancel the report.* "
                await reactionmsg.edit(embed=discord.Embed(description=text, color=self.bot.main_color))

                try:
                    username = await self.bot.wait_for('message', check=checkmsg, timeout=360)
                    if cancel_check(username) is True:
                        cancelEmbed = discord.Embed(description="❌ | Cancelled report", color=15158332)
                        await reactionmsg.edit(embed=cancelEmbed)
                        await reactionmsg.clear_reactions()
                        return
                except asyncio.TimeoutError:

                    return await reactionmsg.edit(embed=embedTimeout)
                await username.delete()

                text = "*Customer/Non-Staff Report**\nWhat is the reason for this report? You have 5 minutes to reply.\n\n*Say " \
                       "'cancel' to cancel the report.* "
                await reactionmsg.edit(embed=discord.Embed(description=text, color=self.bot.main_color, ))

                try:
                    reason = await self.bot.wait_for('message', check=checkmsg, timeout=360)
                    if cancel_check(reason) is True:
                        cancelEmbed = discord.Embed(description="❌ | Cancelled report", color=15158332)
                        await reactionmsg.edit(embed=cancelEmbed)
                        await reactionmsg.clear_reactions()
                        return
                except asyncio.TimeoutError:
                    return await reactionmsg.edit(embed=embedTimeout)
                await reason.delete()

                text = "**Customer/Non-Staff Report**\nPlease provide proof of this happening. You can upload a video/image or use " \
                       "a link to an image or video. The report will be sent right after. You have 10 minutes to " \
                       "reply.\n\n*Say 'cancel' to cancel the report.* "
                await reactionmsg.edit(embed=discord.Embed(description=text, color=self.bot.main_color))

                try:
                    proof = await self.bot.wait_for('message', check=checkmsg, timeout=600)
                    if cancel_check(proof) is True:
                        cancelEmbed = discord.Embed(description="❌ | Cancelled report", color=15158332)
                        await reactionmsg.edit(embed=cancelEmbed)
                        await reactionmsg.clear_reactions()
                        return
                except asyncio.TimeoutError:
                    return await reactionmsg.edit(embed=embedTimeout)
                my_files = [await x.to_file() for x in proof.attachments]
                await proof.delete()

                reportEmbed = discord.Embed(title="New Customer/Non-Staff Report", color=self.bot.main_color)
                reportEmbed.add_field(name="Username:", value=username.content)
                if proof.content:
                    reportEmbed.add_field(name="Proof:", value=proof.content)
                reportEmbed.add_field(name="Reason:", value=reason.content)
                reportEmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar)
                await guestChannel.send(content="---------------------------", embed=reportEmbed, files=my_files)
                text = "✅ | The report has successfully been sent!"
                await reactionmsg.edit(embed=discord.Embed(description=text, color=3066993))

            if str(reaction.emoji) == '❌':
                cancelEmbed = discord.Embed(description="❌ | Cancelled report", color=15158332)
                await reactionmsg.edit(embed=cancelEmbed)
                return await reactionmsg.clear_reactions()
        except discord.ext.commands.CommandOnCooldown:
            print("cooldown")


async def setup(bot):
    await bot.add_cog(Reports(bot))
