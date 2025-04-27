import yaml
from pathlib import Path
import asyncio
import re

from discord.ext import commands
import discord


class PlayerCharacter(commands.Cog):
    def __init__(self, bot, profile_id):
        self.bot = bot
        self._profile_id = profile_id
        self._character_thread = None

        self._quests = []
        self._message_responses = []

        self._last_message = None

        self._setup_subscriptions()

        self.__cog_name__ = f"PlayerCharacter-{profile_id}"

    @property
    def quests(self) -> list:
        return self._quests

    @property
    def level(self) -> int:
        return 3 + int(len(self.quests) / 4)

    async def add_quest(self, quest):
        admin_user_id = 309102962234359829
        admin = self.bot.get_user(admin_user_id)
        this_thread = await self.get_character_thread()

        level_before = self.level
        self._quests.append(quest)

        await admin.send(f"{this_thread.name} went on the quest {quest.name}!")

        if self.level != level_before:
            await admin.send(f"{this_thread.name} by {this_thread.owner.display_name} just hit level {self.level}")


    @commands.Cog.listener(name="on_message")
    async def _handle_quest_message(self, message):
        pattern = (r"https://discord.com/channels/918112437331427358/(?P<quest_thread_url>\d+)|"
                   r"<#(?P<quest_thread_id>\d+)>")

        matches = re.findall(pattern, message.content)
        matches = [item for match in matches for item in match if item]

        for thread_id in matches:
            quest = await self.bot.fetch_channel(thread_id)
            if not hasattr(quest, "parent"):
                continue
            if quest.parent.id != 1290373594781716554:
                continue
            if quest in self._quests:
                continue

            await self.add_quest(quest)

    # async def _handle_last_message(self, message):
    #     # TODO
    #     print(f"_handle_last_message processed {message}")

    def _setup_subscriptions(self):
        self._message_responses.append(self._handle_quest_message)
        # self._message_responses.append(self._handle_last_message)

    async def get_character_thread(self):
        if self._character_thread:
            return self._character_thread

        self._character_thread = await self.bot.fetch_channel(self._profile_id)
        return self._character_thread

    async def process_history(self):
        thread = await self.get_character_thread()
        async for message in thread.history(limit=None):
            await self.process_message(message)

    async def process_message(self, message):
        """Publish data to all subscribers of an event type."""
        for callback in self._message_responses:
            await callback(message)

