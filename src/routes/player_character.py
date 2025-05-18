import re
import os

from discord.ext import commands
import discord

from logic.bastion.bastion import Bastion
from views.bastion.bastion_view import BastionConstructionView, AboutBastionView


class PlayerCharacter(commands.Cog):
    def __init__(self, bot, profile_id: int, player_cog):
        self.bot = bot
        self.profile_id = profile_id
        self.player_cog = player_cog

        self._character_thread = None

        self._quests = set()
        self._message_responses = []

        self._last_message = None

        self.__cog_name__ = f"PlayerCharacter-{profile_id}"

        self.bot.add_command(self.ask_level())

    @classmethod
    async def create(cls, bot, profile_id: int, player_cog):
        self = cls(bot, profile_id, player_cog)
        await self._populate_quest_history()

        current_level = await self.level()
        this_thread = await self.get_character_thread()

        was_updated = [
            msg
            async for msg in this_thread.history(limit=None)
            if f"hit level {current_level}" in msg.content
        ]
        if not was_updated:
            await this_thread.send(f"{this_thread.name} hit level {current_level}! Congrats :)")

        self.bastion = await Bastion.create(owner=self)
        self.bastion_view = await AboutBastionView.create(self.bastion)
        await this_thread.send(embed=self.bastion_view.initial_embed(),
                               view=self.bastion_view)

        return self

    async def _get_quests_from_msg(self, message) -> list[discord.Thread]:
        """

        :param message:
        :type message:
        :return:
        :rtype:
        """
        quests = []

        pattern = (fr"https://discord(?:app)?.com/channels/{os.environ.get('SERVER_ID')}/(?P<quest_thread_url>\d+)|"
                   r"<#(?P<quest_thread_id>\d+)>")

        matches = re.findall(pattern, message.content)
        matches = [item for match in matches for item in match if item]

        for thread_id in matches:
            try:
                quest: discord.Thread = await self.bot.fetch_channel(thread_id)
            except discord.errors.NotFound:
                print(f"Quest not found in message.\n{message.content}")
                continue
            except Exception as e:
                print(f"Encountered an unknown error looking for quest in msg.\n{message.content}")
                continue

            if not hasattr(quest, "parent"):
                continue
            if quest.parent.id not in [int(os.environ.get("QUEST_BOARD_ID")), int(os.environ.get("REQUEST_BOARD_ID"))]:
                continue

            quests.append(quest)

        return quests

    async def quests(self) -> list:
        """
        # TODO: need to search history when this is called
        :return:
        :rtype:
        """
        if not self._quests:
            await self._populate_quest_history()

        return self._quests

    async def _populate_quest_history(self) -> None:
        this_thread = await self.get_character_thread()
        async for message in this_thread.history(limit=None):
            quests = await self._get_quests_from_msg(message)
            for quest in quests:
                if quest in self._quests:
                    continue
                self._quests.add(quest)

    async def _add_quest(self, quest: discord.Thread) -> None:
        this_thread = await self.get_character_thread()

        # Make sure we've initialized the quest from history before we add one
        if not self._quests:
            await self._populate_quest_history()

        level_before = await self.level()
        self._quests.add(quest)
        level_after = await self.level()

        if level_after != level_before:
            await this_thread.send(f"{this_thread.name} hit level {await self.level()}! Congrats :)")

    async def level(self) -> int:
        return 3 + int(len(await self.quests()) / 4)

    async def get_character_thread(self) -> discord.Thread:
        if not self._character_thread:
            self._character_thread = await self.bot.fetch_channel(self.profile_id)

        return self._character_thread

    @commands.Cog.listener(name="on_message")
    async def handle_quest_message(self, message):

        # Only process messages from this character's character profile
        if not self.profile_id or not message.channel.id == self.profile_id:
            return

        quests = await self._get_quests_from_msg(message)
        for quest in quests:
            if quest in self._quests:
                continue
            await self._add_quest(quest)

    @commands.Cog.listener(name="on_message_edit")
    async def _handle_quest_message_update(self, message_before, message_after):
        await self.handle_quest_message(message_after)

    def ask_level(self):
        """
        Wraps dynamic command so that the level for the specific profile id can be queried
        :return:
        :rtype:
        """

        @commands.command(name=f"{self.profile_id}-level")
        async def dynamic_command(ctx):
            admin = self.bot.get_user(int(os.environ.get("ADMIN_ID")))
            this_thread = await self.get_character_thread()

            await admin.send(f"{this_thread.jump_url} by {this_thread.owner.display_name} is level {await self.level()}")

        return dynamic_command
