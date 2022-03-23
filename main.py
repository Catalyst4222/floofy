import asyncio
from time import time

from dis_snek import Intents, Snake, listen

from utilities.actions_config import load_actions
from utilities.global_config import token

# Define bot intents
intents = Intents.DEFAULT | Intents.GUILD_MEMBERS

# Calculate start time
start = time()

# Create bot instance
bot = Snake(default_prefix=("f!", "F!"), intents=intents)

# List of cog extensions
extensions = ["commands.actions"]

# List of action text files
action_text_files = ["pet", "boop"]


@listen()
async def on_startup():
    op_time = round((time() - start), 2)

    print(f"Floofy is ready to serve! (Operation took {op_time} seconds)")
    print(f"Currently logged in as {bot.user} (ID: {bot.user.id})")
    print(f"Current ping to Discord is {round(bot.latency * 1000, 2)}ms")
    await bot.change_presence(activity="Currently under development!")


if __name__ == "__main__":
    load_actions(action_text_files)

    # Load command extension files
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded command extension [{extension}]")
        except Exception as error:
            print(f"{extension} could not be loaded. Stack:\n{error}")

    bot.start(token)
