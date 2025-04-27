# main.py
import time
import os
from datetime import datetime
import asyncio

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


# Load all cogs (commands) when bot is ready
@bot.event
async def on_ready():
    admin_user_id = 309102962234359829
    admin = bot.get_user(admin_user_id)
    await admin.send(f"Bot reset at {datetime.now()}")

    # asyncio.create_task(thirty_minute_process_cycles())
    # asyncio.create_task(weekly_process_cycles())

    # Initialize Player Character Cogs
    player_character_thread_id = 1293034430968889477
    player_character_thread = bot.get_channel(player_character_thread_id)

    characters = []
    older_threads = [thread async for thread in player_character_thread.archived_threads() if thread]
    for thread in player_character_thread.threads + older_threads:
        if not thread.owner:
            # The person has left the server
            continue
        characters.append(PlayerCharacter(bot, thread.id))
        if not bot.get_cog(f"Player-{thread.owner.id}"):
            await bot.add_cog(Player(bot, thread.owner.id))
    for character in characters:
        await character.process_history()
        await bot.add_cog(character)

    quest_board_id = 1290373594781716554
    quest_board_forum = bot.get_channel(quest_board_id)

    request_board_id = 1359554902451425280
    request_board_forum = bot.get_channel(request_board_id)

    # # Initialize Quest Cogs
    quests = []
    for thread in quest_board_forum.threads[::-1] + request_board_forum.threads[::-1]:
        if thread.created_at < (datetime.now() - timedelta(days=5)).replace(tzinfo=timezone.utc):
            break
        quests.append(QuestManager(bot, thread.id))

    quests.append(QuestManager(bot, 1347028121760694393))

    for quest in quests:
        await quest.process_history()
        await bot.add_cog(quest)

    # Initialize Other Cogs
    # for cog in commands.Cog.__subclasses__():
    #     module_name = cog.__module__.split(".")[0]
    #     if module_name == "routes":
    #         await bot.add_cog(cog(bot))

@bot.event
async def on_message(message):
    if "!level" in message.content:
        admin_user_id = 309102962234359829
        admin = bot.get_user(admin_user_id)

        player_cogs = [bot.cogs[cog] for cog in bot.cogs if type(bot.cogs[cog]) == Player]

        for cog in player_cogs:
            await cog.ask_level()(None)


@bot.event
async def on_thread_create(thread):
    CHARACTER_PROFILES_ID = 1293034430968889477
    # Check if the thread is in the target channel
    if thread.parent_id == CHARACTER_PROFILES_ID:
        character = PlayerCharacter(bot, thread.id)
        await bot.add_cog(character)

    QUEST_BOARD_ID = 1290373594781716554
    REQUEST_BOARD_ID = 1359554902451425280
    # Check if the thread is in the target channel
    if thread.parent_id in [QUEST_BOARD_ID, REQUEST_BOARD_ID]:
        quest = QuestManager(bot, thread.id)
        await bot.add_cog(quest)


async def weekly_process_cycles():
    minute = 60
    hour = minute*60
    day = hour*24
    week = day*7
    interval = week

    while True:
        print(f"{datetime.now()} - Running Role Logger")
        await update_role_expiry(bot)
        await check_role_expiry(bot)
        await notify_member_count(bot)
        await notify_new_members(bot)
        await notify_expiring_members(bot)
        await notify_lost_members(bot)
        save_expiry_data(role_expiry)
        print(f"{datetime.now()} - Finished running Role Logger")

        await asyncio.sleep(interval)

    # routines=[routine(bot).process() for routine in Routine.__subclasses__()]
    # for routine in Routine.__subclasses__():
    #     item = routine(bot)
    #     await item.process()
    # await asyncio.gather(routine(bot).process() for routine in Routine.__subclasses__())


bot.run(TOKEN)
