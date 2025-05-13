import os
import asyncio
from datetime import datetime
import logging

from dotenv import load_dotenv
if not os.getenv("ENV"):
    load_dotenv(dotenv_path=".env.test")

import discord
from discord.ext import commands

from properties.config import PREFIX
# add the cogs context for calls to __subclasses__
from routes import *
from routines.player_signup import PlayerSignup
from role_logger import *



TOKEN = os.environ.get("API_TOKEN")
intents = discord.Intents.all()
intents.members = True
intents.reactions = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

player_fact = PlayerFactory(bot)
quest_fact = QuestFactory(bot, player_fact)

@bot.event
async def on_ready():
    admin = bot.get_user(int(os.environ.get("ADMIN_ID")))
    await admin.send(f"Bot reset at {datetime.now()}")

    await bot.add_cog(player_fact)
    await bot.add_cog(quest_fact)
    await bot.add_cog(Shop(bot))

    # Launch the background task
    asyncio.create_task(init_quest_threads(bot, quest_fact))


async def init_quest_threads(bot, quest_factory):
    await bot.wait_until_ready()  # Just to be safe

    for channel_id in (int(os.environ.get("QUEST_BOARD_ID")), int(os.environ.get("REQUEST_BOARD_ID"))):
        forum_channel = bot.get_channel(channel_id)
        if not forum_channel:
            print(f"Could not find channel with ID {channel_id}")
            continue

        for thread in forum_channel.threads[::-1]:
            await quest_factory.get_cog(thread.id)
            await asyncio.sleep(2)


@bot.event
async def on_message(message):
    if "!level" in message.content:
        sidequest_server = bot.get_guild(int(os.environ.get("SERVER_ID")))
        adventurer_role = sidequest_server.get_role(int(os.environ.get("ADVENTURER_ROLE_ID")))
        adventurers = adventurer_role.members

        for adventurer in adventurers:
            player_cog, was_created = await player_fact.get_cog(adventurer.id)
            await player_cog.ask_level()(None)

    if "!update_roles" in message.content:
        print(f"{datetime.now()} - Running Role Logger")
        await update_role_expiry(bot)
        await check_role_expiry(bot)
        await notify_member_count(bot)
        await notify_new_members(bot)
        await notify_expiring_members(bot)
        await notify_lost_members(bot)
        save_expiry_data(role_expiry)
        print(f"{datetime.now()} - Finished running Role Logger")

        await message.delete()

    await bot.process_commands(message)

bot.run(TOKEN)
