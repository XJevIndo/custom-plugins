import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class botPing(commands.Cog):
    """
    Don't ping the chairman!!
    """

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
      for x in message.mentions:
        if x.id == 767935439986098196:
          replyMsg = discord.Embed(
            description = "Please do not ping the Owner. If you need assistance, DM @Latte Modmail and wait for a Support Team to Reply it.\n\nRemember to turn off reply mentions:",
            color = self.bot.main_color
          )
          replyMsg.set_image(url="https://cdn.discordapp.com/attachments/633681171879952384/830772052045725716/aaaaa.gif")

          noReplyMsg = discord.Embed(
            description = "Please do not ping the Owner. If you need assistance, DM @Latte Modmail and wait for a Support Team to Reply it.",
            color = self.bot.main_color,
          )
          if "767935439986098196" in message.content:
           await message.channel.send(content=f"<@!{message.author.id}>", embed=noReplyMsg)
          else:
           await message.channel.send(content=f"<@!{message.author.id}>", embed=replyMsg)
          break
           

def setup(bot):
    bot.add_cog(botPing(bot))
