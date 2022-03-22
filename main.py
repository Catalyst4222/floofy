import discord

from discord.ext import commands
from time import time
from utilities.global_config import token
from utilities.actions_config import load_actions

# Define bot intents
intents = discord.Intents.default()
intents.members = True

# Calculate start time
start = time()

# Create bot instance
bot = commands.Bot(command_prefix=("f!", "F!"), intents=intents, case_insensitive=True)

# List of cog extensions
extensions = [
    "commands.actions"
]

# List of action text files
action_text_files = [
    "pet",
    "boop"
]


@bot.event
async def on_ready():
    op_time = round((time() - start), 2)

    print(f"Floofy is ready to serve! (Operation took {op_time} seconds)")
    print(f"Currently logged in as {bot.user} (ID: {bot.user.id})")
    print(f"Current ping to Discord is {round(bot.latency * 1000, 2)}ms")

    await bot.change_presence(activity=discord.Game(name="Currently under development!"))


if __name__ == '__main__':
    load_actions(action_text_files)

    # Load command extension files
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded command extension [{extension}]")
        except Exception as error:
            print(f"{extension} could not be loaded. Stack:\n{error}")

    bot.run(token)
