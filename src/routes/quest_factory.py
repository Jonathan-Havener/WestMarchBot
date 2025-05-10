import os

import discord
from discord.ext import commands

from .quest_manager import QuestManager
from .player_factory import PlayerFactory


class QuestFactory(commands.Cog):
    def __init__(self, bot: commands.Bot, player_factory: PlayerFactory):
        self.bot = bot
        self.player_factory = player_factory

        self._quest_forums = [
            int(os.environ.get("QUEST_BOARD_ID")),
            int(os.environ.get("REQUEST_BOARD_ID"))
        ]

    async def get_cog(self, quest_id: str):
        quest_cog = self.bot.get_cog(f"Quest-{quest_id}")
        created = False

        if not quest_cog:
            quest_cog = QuestManager(self.bot, quest_id, self.player_factory)
            await self.bot.add_cog(quest_cog)
            created = True

        return quest_cog, created

    @commands.Cog.listener(name="on_thread_create")
    async def _quest_created(self, thread: discord.Thread):
        """
        Creates a quest manager cog and adds it to the bot when a quest is created
        :param thread:
        :type thread:
        :return:
        :rtype:
        """
        if (not isinstance(thread, discord.Thread) or
                not thread.parent or
                thread.parent.id not in self._quest_forums):
            return

        _, _ = await self.get_cog(thread.id)

    @commands.Cog.listener(name="on_message")
    async def _quest_message(self, message: discord.Message):
        """
        Create a quest manager cog when someone sends a message into quest channel that doesn't already have
        a cog
        :param message:
        :type message:
        :return:
        :rtype:
        """
        if not isinstance(message.channel, discord.Thread):
            return

        if message.channel.parent.id not in self._quest_forums:
            return

        quest_cog, is_new = await self.get_cog(message.channel.id)

        if not is_new:
            return

        # Pass the message along to the created quest manager
        for listener in quest_cog.get_listeners():
            key, method = listener

            if key != "on_message":
                continue

            await method(message)

        await quest_cog.process_history()
