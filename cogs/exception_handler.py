import discord
from discord.ext import commands

class ExceptionHandler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error) -> None:
        print(error)
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExceptionHandler(bot))
