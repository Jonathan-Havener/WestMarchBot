import discord
from discord.ext import commands

import secrets_config
from basic_thread import Basic_Thread
import pickle

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
database = {}  # Your database (e.g., could be a dictionary)

YOUR_SPECIFIC_CHANNEL_ID=secrets_config.channel_id


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # check_inactive_users.start()

    channel = bot.get_channel(YOUR_SPECIFIC_CHANNEL_ID)
    data = {}


@bot.event
async def on_thread_create(thread):
    admin_user_id = 309102962234359829
    admin = bot.get_user(admin_user_id)
    if not admin:
        return
    message = await admin.send(f"The thread *{thread.name}* was created in *{thread.parent}*.\n"
                               f"React :one: when this quest has completed.")
    await message.add_reaction("1️⃣")



bot.run(secrets_config.bot_token)
