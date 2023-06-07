import os
import sys
import yaml
import shelve
import asyncio
import discord
from loguru import logger
from discord import app_commands, ui, Embed
from discord.ext import commands, tasks

# Load configuration from YAML file
if os.getenv('DEBUG_SWIM_BOT') == 'true':
    with open('config-dev.yml') as f:
        cfg = yaml.safe_load(f)
else:
    with open('config.yml') as f:
        cfg = yaml.safe_load(f)

# Create a guild object from the guild id in the config file
GUILD_OBJ = discord.Object(id=cfg['guild']) # guild id the bot will be used in 
EMBED_COLOR = discord.Colour.from_rgb(255, 255, 255)

intents = discord.Intents.default()
intents.members = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__("[", intents=intents)
        self.guild = GUILD_OBJ
        self.cfg = cfg
        self.storage = shelve.open('storage', writeback=True) 

    async def setup_hook(self):
        await self.load_extension('cogs.admin')
        await self.sync_commands()

    async def sync_commands(self):
        self.tree.copy_global_to(guild=self.guild)
        await self.tree.sync(guild=self.guild)

bot = Bot()

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')

@tasks.loop(minutes=5)
async def sync_storage():
    logger.debug("Syncing storage...")
    bot.storage.sync()

async def start_client():
    while True:
        if os.getenv('DEBUG_SWIM_BOT') != 'true':   
            try:
                logger.add(sys.stdout, level="DEBUG", enqueue=True)
                logger.info("Starting client...")
                await bot.start(cfg['bot_token'])
            except KeyboardInterrupt:
                logger.info("Caught keyboard interrupt, closing client...")
                await bot.close()
                break
            except Exception as e:
                logger.error(f"Caught an exception: {type(e).__name__} - {e}")
                await asyncio.sleep(5)
        else:
            logger.add(sys.stdout, level="DEBUG", enqueue=True)
            logger.info("Starting client in debug mode...")
            await bot.start(cfg['bot_token'])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(start_client())
    loop.run_forever()

