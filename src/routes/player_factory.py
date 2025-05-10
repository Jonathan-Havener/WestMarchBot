import os

import discord
from discord.ext import commands

from .player import Player


class PlayerFactory(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.brighthaven_category_id = int(os.environ.get("BRIGHTHAVEN_CATEGORY_ID"))

    async def get_cog(self, player_id: str):
        player_cog = self.bot.get_cog(f"Player-{player_id}")
        created = False

        if not player_cog:
            player_cog = Player(self.bot, player_id)
            await self.bot.add_cog(player_cog)
            created = True

        return player_cog, created

    @commands.Cog.listener(name="on_message")
    async def _player_message(self, message: discord.Message):
        """

        :param message:
        :type message:
        :return:
        :rtype:
        """
        if not isinstance(message.channel, discord.abc.GuildChannel) or message.channel.category_id != self.brighthaven_category_id:
            return

        player_cog, is_new = await self.get_cog(message.author.id)

        if not is_new:
            return

        # Pass the message along to the created quest manager
        for listener in player_cog.get_listeners():
            key, method = listener

            if key != "on_message":
                continue

            await method(message)
