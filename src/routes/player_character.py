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

        self.bot.add_command(self.ask_level())

    @property
    def quests(self) -> list:
        return self._quests

    @property
    def level(self) -> int:
        return 3 + int(len(self.quests) / 4)

    def ask_level(self):
        """
        Wraps dynamic command so that the level for the specific profile id can be queried
        :return:
        :rtype:
        """

        @commands.command(name=f"{self._profile_id}-level")
        async def dynamic_command(ctx):
            admin_user_id = 309102962234359829
            admin = self.bot.get_user(admin_user_id)
            this_thread = await self.get_character_thread()

            await admin.send(f"{this_thread.jump_url} by {this_thread.owner.display_name} is level {self.level}")

        return dynamic_command

    async def add_quest(self, quest, notify: bool):
        # admin_user_id = 309102962234359829
        # admin = self.bot.get_user(admin_user_id)
        this_thread = await self.get_character_thread()

        level_before = self.level
        self._quests.append(quest)

        # await admin.send(f"{this_thread.jump_url} went on the quest {quest.jump_url}!")
        #
        if notify and self.level != level_before:
            await this_thread.send(f"{this_thread.name} hit level {self.level}! Congrats :)")

    @commands.Cog.listener(name="on_message")
    async def _handle_quest_message(self, message, notify: bool = True):

        # Only process messages from this character's character profile
        if not self._profile_id or not message.channel.id == self._profile_id:
            return

        pattern = (r"https://discord(?:app)?.com/channels/918112437331427358/(?P<quest_thread_url>\d+)|"
                   r"<#(?P<quest_thread_id>\d+)>")

        matches = re.findall(pattern, message.content)
        matches = [item for match in matches for item in match if item]

        for thread_id in matches:
            try:
                quest = await self.bot.fetch_channel(thread_id)
            except discord.errors.NotFound:
                print(f"Quest not found in message.\n{message.content}")
                continue
            except Exception as e:
                print(f"Encountered an unknown error looking for quest in msg.\n{message.content}")
                continue

            if not hasattr(quest, "parent"):
                continue
            if quest.parent.id not in [1290373594781716554, 1359554902451425280]:
                continue
            if quest in self._quests:
                continue

            await self.add_quest(quest, notify)

    @commands.Cog.listener(name="on_message_edit")
    async def _handle_quest_message_update(self, message_before, message_after):
        await self._handle_quest_message(message_after)

    # async def _handle_last_message(self, message):
    #     # TODO
    #     print(f"_handle_last_message processed {message}")

    def _setup_subscriptions(self):
        """
        This initializes all the responses we may have for a message
        This is primarily used when processing a history of messages sent before the cog was created
        :return:
        :rtype:
        """
        self._message_responses.append(self._handle_quest_message)
        # self._message_responses.append(self._handle_last_message)

    async def get_character_thread(self):
        if self._character_thread:
            return self._character_thread

        self._character_thread = await self.bot.fetch_channel(self._profile_id)
        return self._character_thread

    async def process_history(self):
        this_thread = await self.get_character_thread()
        print(f"Processing quest history for {this_thread.owner.display_name}'s character {this_thread.name}")
        async for message in this_thread.history(limit=None):
            await self.process_message(message)

    async def process_message(self, message):
        """
        This invokes all the on_message methods as if the message was just sent.
        This is used to process history.
        """
        for callback in self._message_responses:
            await callback(message, notify=False)
