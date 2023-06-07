import discord
import aiohttp
import json
from typing import List, TypedDict
from loguru import logger
from discord.ext import commands, tasks
from discord import app_commands as c

serverstatus = None

class ServerData(TypedDict):
    cars: List[str]
    clients: int
    country: List[str]
    cport: int
    durations: List[int]
    extra: bool
    inverted: int
    ip: str
    json: None
    l: bool
    maxclients: int
    name: str
    has_pass: bool
    pickup: bool
    pit: bool
    port: int
    session: int
    sessiontypes: List[int]
    timed: bool
    timeleft: int
    timeofday: int
    timestamp: int
    tport: int
    track: str
    poweredBy: str

async def serialize(server_data: ServerData) -> str:
    def default_encoder(obj):
        if isinstance(obj, TypedDict):
            return dict(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    return json.dumps(server_data, default=default_encoder, indent=4)

async def deserialize(json_str: str) -> ServerData:
    def object_hook(obj):
        if "cars" in obj:
            obj["has_pass"] = obj["pass"]
            return ServerData(obj)
        return obj
    return json.loads(json_str, object_hook=object_hook)

class ServerStatus(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.port_range = range(self.client.cfg["port_range"][0], self.client.cfg["port_range"][1] + 1)

    async def server_status(self):
        logger.debug("Getting server status...")
        all_status = []
        async with aiohttp.ClientSession() as session:
            for p in self.port_range:
                try:
                    async with session.get(f'http://127.0.0.1:{p}/INFO') as resp:
                        if resp.status == 200:
                            all_status.append(await deserialize(await resp.text())) 
                except Exception as e:
                    logger.error(f"Exception occured while fetching server status: {e}")
                    continue
        return all_status

    @c.command()
    @c.checks.has_permissions(administrator=True)
    async def create_status_message(self, interaction: discord.Interaction):
        logger.debug("Creating status message...")
        self.client.storage["status_message_channel"] = interaction.channel.id
        status = await self.server_status()
        embed = discord.Embed(title="Server Status", description="Status of all servers", color=0x00ff00)
        for s in status:
            embed.add_field(name=s["name"], value=f"**Track:** {s['track']}\n**Session:** {s['session']}\n**Time left:** {s['timeleft']}\n**Cars:** {s['clients']}/{s['maxclients']}", inline=False, url=f" https://acstuff.ru/s/q:race/online/join?ip={s['ip']}&httpPort={s['cport']}")
        message = await interaction.response.send_message(embed=embed)
        self.client.storage["status_message"] = message.id

    @tasks.loop(minutes=1)
    async def update_status_message(self):
        logger.debug("Updating status message...")
        status = await self.server_status()
        embed = discord.Embed(title="Server Status", description="Status of all servers", color=0x00ff00)
        for s in status:
            embed.add_field(name=s["name"], value=f"**Track:** {s['track']}\n**Session:** {s['session']}\n**Time left:** {s['timeleft']}\n**Cars:** {s['clients']}/{s['maxclients']}", inline=False, url=f" https://acstuff.ru/s/q:race/online/join?ip={s['ip']}&httpPort={s['cport']}")
        message = await self.client.get_channel(self.client.storage["status_message_channel"]).fetch_message(self.client.storage["status_message"])
        await message.edit(embed=embed)
        logger.debug("Status message updated!")

async def setup(bot):
    global serverstatus
    serverstatus = ServerStatus(bot)
    await bot.add_cog(serverstatus)
    serverstatus.update_status_message.start()
