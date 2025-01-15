# main.py

import discord
from discord.ext import commands
import json
from properties.config import TOKEN, PREFIX
from src.wm_logging import gen_logger
from properties.NewDevlinProperties import *
#from properties.righthavenProperties import *

intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await update_role_expiry()
    await bot.close()  # Close the bot after the check

quest_info = {
    "dms": {},
    "players": {}
}

async def update_role_expiry():
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        gen_logger.error(f"Guild not found!")
        return

    for channel in guild.channels:
        if channel.id == QUEST_CHANNEL_ID:

            gen_logger.debug(f"Processing archived threads.")
            # Fetch archived threads
            async for thread in channel.archived_threads(limit=None):
                await process_thread(thread)

            gen_logger.debug(f"Processing active threads.")
            # Fetch active threads
            for thread in channel.threads:
                await process_thread(thread)

            with open("users.json", "w") as file:
                json.dump(quest_info, file, indent=4)


async def process_thread(thread):
    host = thread.owner.nick if hasattr(thread.owner, "nick") else thread.owner.name if hasattr(thread.owner, "name") else "Unknown"

    if host not in quest_info["dms"]:
        quest_info["dms"][host] = []

    quest_info["dms"][host].append({
        "quest": thread.name,
        "date": str(thread.created_at)
    })

    players = []
    async for message in thread.history(limit=None):
        player_name = message.author.nick if hasattr(message.author, "nick") else message.author.name if hasattr(message.author, "name") else "Unknown"
        if player_name != host:
            players.append(player_name)

    for player in players:
        if player not in quest_info["players"]:
            quest_info["players"][player] = []
        quest_info["players"][player].append({
            "quest": thread.name,
            "date": str(thread.created_at)
    })


import matplotlib.pyplot as plt
def generate_level_histograms():
    quest_objs = generate_quest_objects()
    levels = [(num, quest.adventure_date) for quest in quest_objs for num in quest.level_range]
    level_list = sorted(set(level for level, _ in levels))

    for level in level_list:
        level_data = [date for l, date in levels if l == level]
        plt.figure(figsize=(6, 3))
        plt.hist(level_data, bins=12, alpha=0.5)
        plt.title(f'Frequency of Level {level} Over Time')
        plt.xlabel('Date')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    print("Done")

bot.run(TOKEN)
