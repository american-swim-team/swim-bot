 # Swim Bot
 
 Swim Bot is a Discord bot developed to enhance the functionality of a specific guild. It provides various features and commands to manage and interact with the guild. The bot is built using Python and utilizes the Discord.py library.
 
 ## Installation
 
 1. Clone the repository:
 
    ```shell
    git clone https://github.com/example/swim-bot.git
    ```
 
 2. Navigate to the project directory:
 
    ```shell
    cd swim-bot
    ```
 
 3. Install the dependencies using Poetry:
 
    ```shell
    poetry install
    ```
 
    This will install all the required packages for the bot.
 
 4. Configure the bot:
 
    - Rename the `config.yml.example` file to `config.yml`.
    - Edit the `config.yml` file and provide your Discord bot token and the guild ID where you want to use the bot.
 
 5. Run the bot:
 
    ```shell
    poetry run python bot.py
    ```
 
    The bot should now be online and ready to use in the specified guild.
 
 ## Usage
 
 Once the bot is running and connected to your guild, you can interact with it using various commands. The bot uses slash commands (/) instead of a command prefix.
 
 Here are some of the available commands:
 
 - `/ping`: Responds with "Pong!" to check if the bot is responsive.
 - `/load_cog <cog>`: Loads the specified cog. Only administrators have permission to use this command.
 - `/unload_cog <cog>`: Unloads the specified cog. Only administrators have permission to use this command.
 - `/reload_cog <cog>`: Reloads the specified cog. Only administrators have permission to use this command.
 - `/list_cogs`: Lists the loaded and unloaded cogs. Only administrators have permission to use this command.
 
 ## Cogs
 
 The bot utilizes a modular architecture called "cogs" to organize and separate different sets of commands and features. Each cog represents a specific category or functionality.
 
 ### Admin Cog
 
 The admin cog provides commands related to managing other cogs and their functionalities. It includes the following commands:
 
 - `/ping`: Responds with "Pong!" to check if the bot is responsive.
 - `/load_cog <cog>`: Loads the specified cog. Only administrators have permission to use this command.
 - `/unload_cog <cog>`: Unloads the specified cog. Only administrators have permission to use this command.
 - `/reload_cog <cog>`: Reloads the specified cog. Only administrators have permission to use this command.
 - `/list_cogs`: Lists the loaded and unloaded cogs. Only administrators have permission to use this command.
 
 You can extend the bot's functionality by creating additional cogs and adding them to the `cogs` directory. Each cog should be defined in a separate Python file and follow the Discord.py [cog structure](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html).
 
 ## License
 
 This project is licensed under the MIT License. View the [LICENSE](LICENSE) file for more details.

