import os
import discord
from loguru import logger
from discord.ext import commands
from discord import app_commands as c

class Admin(commands.Cog):
    def __init__(self, bot):
        self.client = bot
        self.tree = bot.tree

    @c.command()
    async def ping(self, interaction: discord.Interaction):
        logger.debug("Pong!")
        await interaction.response.send_message("Pong!", ephemeral=True)

    @c.command()
    @c.checks.has_permissions(administrator=True)
    async def load_cog(self, interaction: discord.Interaction, cog: str):
        logger.debug(f"Loading cog {cog}...")
        try:
            await self.client.load_extension(f"cogs.{cog}")
            await self.client.sync_commands()
        except Exception as e:
            logger.error(f"Exception occured: {e}")
            await interaction.response.send_message(f"Exception occured: \n{e}", ephemeral=True)
        await interaction.response.send_message(f"Loaded {cog}.", ephemeral=True)

    @c.command()
    @c.checks.has_permissions(administrator=True)
    async def unload_cog(self, interaction: discord.Interaction, cog: str):
        logger.debug(f"Unloading cog {cog}...")
        try:
            if cog == "admin":
                await interaction.response.send_message("You can't unload the admin cog.", ephemeral=True)
                return
            await self.client.unload_extension(f"cogs.{cog}")
            await self.client.sync_commands()
        except Exception as e:
            logger.error(f"Exception occured: {e}")
            await interaction.response.send_message(f"Exception occured: \n{e}", ephemeral=True)
        await interaction.response.send_message(f"Unloaded {cog}.", ephemeral=True)

    @c.command()
    @c.checks.has_permissions(administrator=True)
    async def reload_cog(self, interaction: discord.Interaction, cog: str):
        logger.debug(f"Reloading cog {cog}...")
        try:
            await self.client.reload_extension(f"cogs.{cog}")
            await self.client.sync_commands()
        except Exception as e:
            logger.error(f"Exception occured: {e}")
            await interaction.response.send_message(f"Exception occured: \n{e}", ephemeral=True)
        await interaction.response.send_message(f"Reloaded {cog}.", ephemeral=True)

    @c.command()
    @c.checks.has_permissions(administrator=True)
    async def list_cogs(self, interaction: discord.Interaction):
        logger.debug("Listing cogs...")
        cogs = self.client.extensions
        unloaded_cogs = os.listdir("cogs")
        if '__pycache__' in unloaded_cogs:
            unloaded_cogs.remove('__pycache__')
        logger.debug(f"Loaded cogs: {', '.join(cogs)}\nUnloaded Cogs: {', '.join(unloaded_cogs)}")
        await interaction.response.send_message(f"Loaded cogs: {', '.join(cogs)}\nUnloaded Cogs: {', '.join(unloaded_cogs)}", ephemeral=True)

async def setup(bot):
    logger.debug("Loading admin cog...")
    await bot.add_cog(Admin(bot))
