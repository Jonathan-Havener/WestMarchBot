import os

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


@bot.event
async def on_ready():
    admin_user_id = 309102962234359829
    admin = bot.get_user(admin_user_id)
    await admin.send(f"Bot reset at {datetime.now()}")

    await bot.add_cog(QuestFactory(bot))

    # Initialize Player Character Cogs
    # player_character_thread_id = 1293034430968889477
    # player_character_thread = bot.get_channel(player_character_thread_id)

    # characters = []
    # older_threads = [thread async for thread in player_character_thread.archived_threads() if thread]
    # for thread in player_character_thread.threads + older_threads:
    #     if not thread.owner:
    #         # The person has left the server
    #         continue
    #     characters.append(PlayerCharacter(bot, thread.id))
    #     if not bot.get_cog(f"Player-{thread.owner.id}"):
    #         await bot.add_cog(Player(bot, thread.owner.id))
    # for character in characters:
    #     await character.process_history()
    #     await bot.add_cog(character)

    # quest_board_id = 1290373594781716554
    # quest_board_forum = bot.get_channel(quest_board_id)
    #
    # request_board_id = 1359554902451425280
    # request_board_forum = bot.get_channel(request_board_id)
    #
    # # # Initialize Quest Cogs
    # quests = []
    # for thread in quest_board_forum.threads[::-1] + request_board_forum.threads[::-1]:
    #     # if thread.created_at < (datetime.now() - timedelta(days=5)).replace(tzinfo=timezone.utc):
    #     #     break
    #     quests.append(QuestManager(bot, thread.id))
    #
    # BONUS_EXP_QUEST_ID = 1347028121760694393
    # quests.append(QuestManager(bot, BONUS_EXP_QUEST_ID))
    #
    # for quest in quests:
    #     await quest.process_history()
    #     await bot.add_cog(quest)


async def get_adventurer_cog(id) -> Player:
    player_cog = bot.get_cog(f"Player-{id}")
    if not player_cog:
        player_cog = Player(bot, id)
        await bot.add_cog(player_cog)
    return player_cog


@bot.event
async def on_message(message):
    if "!level" in message.content:
        sidequest_server = bot.get_guild(918112437331427358)
        adventurer_role = sidequest_server.get_role(1297995766350090311)
        adventurers = adventurer_role.members

        for adventurer in adventurers:
            player_cog = await get_adventurer_cog(adventurer.id)
            await player_cog.ask_level()(None)
            return

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


# @bot.event
# async def on_thread_create(thread):
#     CHARACTER_PROFILES_ID = 1293034430968889477
#     # Check if the thread is in the target channel
#     if thread.parent_id == CHARACTER_PROFILES_ID:
#         character = PlayerCharacter(bot, thread.id)
#         await bot.add_cog(character)
#
#     QUEST_BOARD_ID = 1290373594781716554
#     REQUEST_BOARD_ID = 1359554902451425280
#     # Check if the thread is in the target channel
#     if thread.parent_id in [QUEST_BOARD_ID, REQUEST_BOARD_ID]:
#         quest = QuestManager(bot, thread.id)
#         await bot.add_cog(quest)


bot.run(TOKEN)
