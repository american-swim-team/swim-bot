import discord
from discord import app_commands as c
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @c.command()
    async def test(self, interaction: discord.Interaction):
        await interaction.response.send_message("Eureka!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Test(bot))
