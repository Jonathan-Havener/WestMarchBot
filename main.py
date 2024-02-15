import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta

import secrets

from basic_thread import Basic_Thread

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
database = {}  # Your database (e.g., could be a dictionary)

YOUR_SPECIFIC_CHANNEL_ID=secrets.channel_id

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # check_inactive_users.start()

    channel = bot.get_channel(YOUR_SPECIFIC_CHANNEL_ID)
    data = {}
    for thread in channel.threads:
        print(f"Processing Thread {thread.name}")
        # data.update({thread.name:{"thread": thread, "messages": [message async for message in thread.history(after=None)]}})
        data.update({thread.name: Basic_Thread(thread, [message async for message in thread.history(after=None)] )})
    async for thread in channel.archived_threads(limit=9999):
        print(f"Processing Thread {thread.name}")
        # data.update({thread.name:{"thread": thread, "messages": [message async for message in thread.history(after=None)]}})
        data.update({thread.name: Basic_Thread(thread, [message async for message in thread.history(after=None)])})
    data


@bot.event
async def on_message(message):
    # Check if the message is in the specific channel and is a thread creation
    if message.channel.parent.id == YOUR_SPECIFIC_CHANNEL_ID and \
            type(message.channel) is discord.threads.Thread:
        print(message.content)

        #thread_id = message.reference.channel_id
        # database[message.author.id] = {
        #     'thread_id': thread_id,
        #     'last_response': datetime.utcnow()
        # }
        print("Break")


# @tasks.loop(seconds=3)  # Adjust the loop interval as needed
# async def check_inactive_users():
#     pass
    # print("test")
    # for user_id, data in database.copy().items():
    #     last_response_time = data['last_response']
    #     if datetime.utcnow() - last_response_time > timedelta(days=30):
    #         user = bot.get_user(user_id)
    #         thread_id = data['thread_id']
    #
    #         # Direct message the user
    #         await user.send("You haven't responded to the thread in over a month!")
    #
    #         # Forward the user's last response to a specific channel
    #         channel = bot.get_channel(YOUR_SPECIFIC_CHANNEL_ID)
    #         thread_channel = bot.get_channel(thread_id)
    #         last_response = await thread_channel.fetch_message(thread_id)
    #         await channel.send(f"{user.name}'s last response:\n{last_response.content}")
    #
    #         # Remove the user from the database
    #         del database[user_id]


# @check_inactive_users.before_loop
# async def before_check_inactive_users():
#     await bot.wait_until_ready()

bot.run(secrets.bot_token)
