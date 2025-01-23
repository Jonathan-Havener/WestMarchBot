# main.py

import discord
from discord.ext import commands
from properties.config import TOKEN, PREFIX
# add the cogs context for calls to __subclasses__
from routines import *

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


# Load all cogs (commands) when bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

    for cog in commands.Cog.__subclasses__():
        module_name = cog.__module__.split(".")[0]
        if module_name == "routes":
            await bot.add_cog(cog(bot))

    # routines=[routine(bot).process() for routine in Routine.__subclasses__()]
    # for routine in Routine.__subclasses__():
    #     item = routine(bot)
    #     await item.process()
    # await asyncio.gather(routine(bot).process() for routine in Routine.__subclasses__())


bot.run(TOKEN)
