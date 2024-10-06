# main.py

import discord
from discord.ext import commands
from datetime import datetime, timedelta
import json
import os
from config import TOKEN, PREFIX, channel_id
import asyncio

intents = discord.Intents.all()
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

CHANNEL_ID = 1064019917579497592  # Replace with your category ID
ROLE_NAME = 'Season 6 Adventurer'

MAX_CONCURRENT_TASKS = 16
semaphore = asyncio.Semaphore(MAX_CONCURRENT_TASKS)
semaphore1 = asyncio.Semaphore(2)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await check_role_expiry()
    await bot.close()  # Close the bot after the check


async def check_role_expiry():
    guild = bot.get_guild(918112437331427358)
    if not guild:
        print(f"Guild not found!")
        return

    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    seasons = {
        "Season 6 Adventurer": {
            "newest_date": datetime(2024, 6, 30),
            "oldest_date": datetime(2024, 4, 1)
        },
        "Season 5 Adventurer": {
            "newest_date": datetime(2024, 3, 31),
            "oldest_date": datetime(2024, 1, 1)
        },
        "Season 4 Adventurer": {
            "newest_date": datetime(2023, 12, 31),
            "oldest_date": datetime(2023, 10, 1)
        },
        "Season 3 Adventurer": {
            "newest_date": datetime(2023, 9, 30),
            "oldest_date": datetime(2023, 7, 1)
        },
        "Season 2 Adventurer": {
            "newest_date": datetime(2023, 6, 30),
            "oldest_date": datetime(2023, 4, 1)
        },
        "Season 1 Adventurer": {
            "newest_date": datetime(2023, 3, 31),
            "oldest_date": datetime(2023, 1, 1)
        }
    }

    for channel in guild.channels:
        if channel.id == CHANNEL_ID:
            tasks = []

            # Fetch archived threads

            async for thread in channel.archived_threads(limit=None):
                for role_name in seasons:
                    if seasons[role_name]["oldest_date"] < thread.created_at.replace(tzinfo=None) < seasons[role_name]["newest_date"]:
                        role = discord.utils.get(guild.roles, name=role_name)
                        tasks.append(process_thread(thread, role))

            # Fetch active threads
            for thread in channel.threads:
                for role_name in seasons:
                    if seasons[role_name]["oldest_date"] < thread.created_at.replace(tzinfo=None) < seasons[role_name]["newest_date"]:
                        role = discord.utils.get(guild.roles, name=role_name)
                        tasks.append(process_thread(thread, role))

            await asyncio.gather(*tasks)


async def process_thread(thread, role):
    async with semaphore:
        print(f"Processing thread : {thread.name}")
        async for message in thread.history(limit=None):
            if not hasattr(message.author, "roles"):
                print(message.author)
            if message.author.id != thread.owner_id and ROLE_NAME not in message.author.roles:
                await message.author.add_roles(role)
            await asyncio.sleep(1)

bot.run(TOKEN)
