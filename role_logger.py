# main.py

import discord
from discord import utils
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import json
from properties.config import TOKEN, PREFIX
from wm_logging import gen_logger
#from NewDevlinProperties import *
from properties.BrighthavenProperties import *

intents = discord.Intents.all()
intents.members = True
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


def load_expiry_data():
    data = {}
    if not expiry_path.exists():
        data = {}
        data.update({
            "role_duration": role_duration,
            "active users": {},
            "new users": {},
            "expired users": {}
        })
    else:
        with open(expiry_path, 'r') as file:
            data = json.load(file)
    return data


def save_expiry_data(data):
    with open(expiry_path, 'w') as file:
        json.dump(data, file)


role_expiry = load_expiry_data()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await update_role_expiry()
    await check_role_expiry()
    await notify_member_count()
    await notify_new_members()
    await notify_expiring_members()
    await notify_lost_members()
    save_expiry_data(role_expiry)
    await bot.close()  # Close the bot after the check


async def notify_member_count():
    channel = bot.get_channel(bot_updates_channel_id)

    message = f"This campaign currently has {len(role_expiry['active users'])} Adventurers!"

    if channel:
        await channel.send(message)


async def notify_new_members():
    if len(role_expiry['new users']) == 0:
        return

    channel = bot.get_channel(bot_updates_channel_id)

    new_members = '\n'.join(['- ' + member for member in role_expiry['new users'].keys()])

    message = (f"Welcome {len(role_expiry['new users'])} New Adventurers!\n"
               f"{new_members}")

    if channel:
        await channel.send(message)


async def notify_expiring_members():
    channel = bot.get_channel(bot_updates_channel_id)
    if len(role_expiry['expiring users']) == 0:
        return

    expiring_members = '\n'.join(
        [
            f"- {member} has "
            f"{(datetime.fromisoformat(role_expiry['expiring users'][member]) + timedelta(days=90) - datetime.utcnow().replace(tzinfo=timezone.utc)).days}"
            f" days to join a quest!"
            for member in role_expiry['expiring users'].keys()
            ])

    message = (f"{len(role_expiry['expiring users'])} "
               f"{'have licenses' if len(role_expiry['expiring users']) > 1 else 'has a license'} "
               f"expiring in the next {role_warning} days.\n"
               f"{expiring_members}")

    if channel:
        await channel.send(message)


async def notify_lost_members():
    if len(role_expiry['expired users']) == 0:
        return

    channel = bot.get_channel(bot_updates_channel_id)

    fallen_members = '\n'.join(['- ' + member for member in role_expiry['expired users'].keys()])

    message = (f"Rest in peace, our {len(role_expiry['expired users'])} fallen adventurers. "
               f"It has been more than {role_duration} days since we've seen you.\n"
               f"{fallen_members}")

    if channel:
        await channel.send(message)


async def update_role_expiry():
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        gen_logger.error(f"Guild not found!")
        return

    role = discord.utils.get(guild.roles, name=ROLE_NAME)

    if not role:
        gen_logger.error(f"Role not found!")
        return

    for channel in guild.channels:
        if channel.id == QUEST_CHANNEL_ID:
            oldest_date = datetime.utcnow() - timedelta(days=role_duration)
            gen_logger.debug(f"Going back in time to {oldest_date}")

            gen_logger.debug(f"Processing archived threads.")
            # Fetch archived threads
            async for thread in channel.archived_threads(limit=None):
                if thread.created_at.replace(tzinfo=None) > oldest_date:
                    await process_thread(thread, role)

            gen_logger.debug(f"Processing active threads.")
            # Fetch active threads
            for thread in channel.threads:
                await process_thread(thread, role)


async def check_role_expiry():
    role_expiry["expired users"] = {}
    role_expiry["expiring users"] = {}
    role_expiry["new users"] = {}

    guild = bot.get_guild(GUILD_ID)
    if not guild:
        gen_logger.error(f"Guild not found!")
        return

    role = discord.utils.get(guild.roles, name=ROLE_NAME)

    if not role:
        gen_logger.error(f"Role not found!")
        return

    for member, expiry_date in list(role_expiry["active users"].items()):
        message_date = datetime.strptime(expiry_date.split("+")[0].split(".")[0], '%Y-%m-%dT%H:%M:%S')

        user_expiration_date = message_date + timedelta(days=role_duration)
        user_warning_date = user_expiration_date - timedelta(days=role_warning)

        member = utils.get(guild.members, name=member)
        if not member:
            gen_logger.warning(f"User {member} in {EXPIRY_FILE} but couldn't be found in the guild.")
            continue
        if role not in member.roles:
            continue

        if datetime.utcnow() > user_expiration_date:
            role_expiry["expired users"][member.name] = role_expiry["active users"][member.name]
            del role_expiry["active users"][member.name]

        elif datetime.utcnow() > user_warning_date:
            role_expiry["expiring users"][member.name] = role_expiry["active users"][member.name]

    users_in_role = [member.name for member in role.members]
    expired_users = set(users_in_role) - set(role_expiry["active users"].keys())
    for expired_user in expired_users:
        member = utils.get(guild.members, name=expired_user)
        if member.name not in role_expiry["expired users"]:
            role_expiry["expired users"][member.name] = datetime.utcnow().isoformat()
        gen_logger.info(f"[EXPIRY] {member}'s adventuring license has expired!")
        await member.remove_roles(role)


async def process_thread(thread, role):

    async for message in thread.history(limit=None):
        if message.author.id != thread.owner_id:
            message_date = message.created_at.isoformat()

            if str(message.author) not in role_expiry["active users"]:
                if role not in message.author.roles:
                    role_expiry["new users"][str(message.author.name)] = message_date
                    await message.author.add_roles(role)
                    gen_logger.info(f"[NEW USER] Adding new user {message.author.name}")
                gen_logger.debug(f"Adding user {message.author.name} to memory.")
                role_expiry["active users"][str(message.author.name)] = message_date
            elif message_date > role_expiry["active users"][str(message.author.name)]:
                gen_logger.debug(f"Updating expiry for {message.author.name}")
                role_expiry["active users"][str(message.author.name)] = message_date


bot.run(TOKEN)
