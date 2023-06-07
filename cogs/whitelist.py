import shelve
import asyncio
import discord
from loguru import logger
from discord import app_commands as c
from discord import ui, Embed
from discord.ext import commands

def check_steam_id(steam_id):
    if len(steam_id) != 17:
        return True
    try:
        int(steam_id)
    except ValueError:
        return True
    return False

class SteamIDView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label='Whitelist Steam ID ✅', custom_id='update_steam_id', style=discord.ButtonStyle.primary)
    async def button1(self, interaction, button):
        await interaction.response.send_modal(SteamIDModal())

class SteamIDModal(ui.Modal, title='Steam 64 ID'):
    answer = ui.TextInput(label='Enter your ID here', row=1)
    
    async def on_submit(self, interaction: discord.Interaction):
        steam_id = self.answer.value
        
        if check_steam_id(steam_id):
            await interaction.response.send_message(f'Invalid Steam 64 ID!', ephemeral=True)
            return

        user_id = interaction.user.id
        member = await whitelist.guild.get_member(user_id)
        if [role.id for role in member.roles] in whitelist.whitelist_roles:
            whitelist.db["whitelist"][user_id] = steam_id
            await whitelist.update_whitelist()

            await interaction.response.send_message(f'Successfully updated your Steam 64 ID!', ephemeral=True)
        else:
            await interaction.response.send_message(f'Sorry, you need the Olympic subscription to continue!', ephemeral=True) 

class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = shelve.open("whitelist", writeback=True)

    async def setup(self):
        self.guild = self.bot.cfg["guild"]
        self.mod_roles = self.bot.cfg["mod_roles"]
        self.whitelist_roles = self.bot.cfg["whitelist_roles"]
        logger.info("Whitelist cog loaded")

    async def update_whitelist(self):
        guild = self.bot.get_guild(self.guild)
        with open("whitelist.txt", "w") as f:
            for x in self.db['perma_whitelist']:
                for steam_id in self.db['perma_whitelist'][x]:
                    f.write(f"{steam_id}\n")
            for role in self.whitelist_roles:
                role = guild.get_role(role)
                for member in role.members:
                    if member.id in self.db['whitelist']:
                        f.write(f"{self.db['whitelist'][member.id]}\n")

    async def load_whitelist(self):
        logger.debug("Loading whitelist")
        proc = await asyncio.create_subprocess_shell('./refresh-whitelist.sh', stderr=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        if stderr:
            logger.error(f'[stderr]\n{stderr.decode()}')

    @c.command()
    async def add_steamid(self, interaction: discord.Interaction, steam_id: str):
        logger.debug(f"Adding steam id {steam_id}")
        guild = self.bot.get_guild(self.guild)
        user_id = interaction.user.id
        member = await guild.fetch_member(user_id)
        if check_steam_id(steam_id):
            await interaction.response.send_message("Invalid Steam 64 ID!", ephemeral=True)
            return
        # If user can manipulate perma whitelist
        if any([role.id in self.whitelist_roles for role in member.roles]) or interaction.permissions.administrator:
            logger.debug(f"User {user_id} can manipulate perma-whitelist")
            # this looks like bad coding but its because of shelves writeback
            if int(steam_id) not in self.db["perma_whitelist"][user_id]:
                self.db["perma_whitelist"][user_id].append(int(steam_id))
                self.db.sync()
            else:
                await interaction.response.send_message("Steam ID already in whitelist.", ephemeral=True)
                return
            await self.update_whitelist()
            await self.load_whitelist()
        # If user is an olympian
        elif [role.id for role in member.roles] in self.whitelist_roles:
            logger.debug(f"User {user_id} is an olympian")
            self.db["whitelist"][user_id] = int(steam_id)
            await self.update_whitelist()
            await self.load_whitelist()
        else:
            await interaction.response.send_message("You don't have permission to add a steam id.", ephemeral=True)
            return
        await interaction.response.send_message(f"Added {steam_id} to the whitelist!", ephemeral=True)

    @c.command()
    async def remove_steamid(self, interaction: discord.Interaction, steam_id: str):
        logger.debug(f"Removing steam id {steam_id}")
        guild = self.bot.get_guild(self.guild)
        user_id = interaction.user.id
        member = await guild.fetch_member(user_id)
        if check_steam_id(steam_id):
            await interaction.response.send_message("Invalid Steam 64 ID!", ephemeral=True)
            return
        # If user can manipulate perma whitelist
        if any([role.id in self.whitelist_roles for role in member.roles]) or interaction.permissions.administrator:
            logger.debug(f"User {user_id} can manipulate perma-whitelist")
            try:
                if int(steam_id) in self.db["perma_whitelist"][user_id]:
                    self.db["perma_whitelist"][user_id].remove(int(steam_id))
                    self.db.sync()
                else:
                    await interaction.response.send_message("Steam ID not in whitelist.", ephemeral=True)
                    return
            except KeyError:
                await interaction.response.send_message("Steam ID not in whitelist.", ephemeral=True)
                return
            await self.update_whitelist()
            await self.load_whitelist()
        # If user is an olympian
        elif [role.id for role in member.roles] in self.whitelist_roles:
            logger.debug(f"User {user_id} is an olympian")
            try:
                del self.db["whitelist"][user_id]
                self.db.sync()
            except KeyError:
                await interaction.response.send_message("Steam ID not in whitelist.", ephemeral=True)
                return
            await self.update_whitelist()
            await self.load_whitelist()
        else:
            await interaction.response.send_message("You don't have permission to remove a steam id.", ephemeral=True)
            return
        await interaction.response.send_message(f"Removed {steam_id} from the whitelist!", ephemeral=True)

    @c.command()
    @c.checks.has_permissions(administrator=True)
    async def create_steamid_button(self, interaction: discord.Interaction):
        logger.debug(f"User {interaction.user.id} requested whitelist button")
        try:
            view=SteamIDView()
            msg = Embed(title='Whitelist for Olympic', colour=discord.Colour.blue(), description="Click the button below to add your Steam ID to the whitelist, if you don't know how to find your Steam ID click the title, or use a tool such as steamid.io. Should the button below not work please use the /whitelist command.", url="https://nodecraft.com/support/games/steam/how-to-quickly-find-steam-id-numbers") 
        # Send the message and add the button
            message = await interaction.response.send_message('', embed=msg, view=view)
        except Exception as e:
            print(e)

    @c.command()
    async def list_whitelist(self, interaction: discord.Interaction, discord_user: discord.User):
        logger.debug(f"User {interaction.user.id} requested whitelist for {discord_user.id}")
        if any([role.id in self.whitelist_roles for role in interaction.user.roles]) or interaction.permissions.administrator: 
            if discord_user.id in self.db['perma_whitelist']:
                await interaction.response.send_message(f"Perma Whitelist: {self.db['perma_whitelist'][discord_user.id]}", ephemeral=True)
                return
            elif discord_user.id in self.db['whitelist']:
                await interaction.response.send_message(f"Whitelist: {self.db['whitelist'][discord_user.id]}", ephemeral=True)
                return
            else:
                await interaction.response.send_message("User not in whitelist.", ephemeral=True)
                return
        else:
            await interaction.response.send_message("You don't have permission to view the whitelist.", ephemeral=True)
            return

    @c.command()
    @c.checks.has_permissions(administrator=True)
    async def refresh_whitelist(self, interaction: discord.Interaction):
        logger.debug("Refreshing whitelist...")
        await self.update_whitelist()
        await self.load_whitelist()
        await interaction.response.send_message("Whitelist refreshed.", ephemeral=True)

async def setup(bot):
    global whitelist
    whitelist = Whitelist(bot)
    await bot.add_cog(whitelist)
    await whitelist.setup()
