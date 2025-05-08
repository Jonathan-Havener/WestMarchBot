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

player_fact = PlayerFactory(bot)
quest_fact = QuestFactory(bot, player_fact)

@bot.event
async def on_ready():
    admin_user_id = 309102962234359829
    admin = bot.get_user(admin_user_id)
    await admin.send(f"Bot reset at {datetime.now()}")

    await bot.add_cog(player_fact)
    await bot.add_cog(quest_fact)


@bot.event
async def on_message(message):
    if "!level" in message.content:
        sidequest_server = bot.get_guild(918112437331427358)
        adventurer_role = sidequest_server.get_role(1297995766350090311)
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


bot.run(TOKEN)
