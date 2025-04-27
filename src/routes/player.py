import yaml
from pathlib import Path
import asyncio
import re
import time

from discord.ext import commands
import discord


class Player(commands.Cog):
    def __init__(self, bot, player_id):
        self.bot = bot
        self._player_id = player_id

        self.bot.add_command(self.ask_level())

        self.__cog_name__ = f"Player-{player_id}"

        self._player_characters = []
        self._player_cogs = []

    async def player_characters(self):
        if not self._player_characters:
            QUESTBOARD_ID = 1293034430968889477
            questboard = self.bot.get_channel(QUESTBOARD_ID)

            older_threads = [thread async for thread in questboard.archived_threads() if thread]
            self._player_characters = [
                thread
                for thread in questboard.threads + older_threads
                if thread.owner and thread.owner.id == self._player_id
            ]
        return self._player_characters

    async def player_cogs(self):
        if not self._player_cogs:
            _player_cogs = []
            for character_thread in await self.player_characters():
                character_cog = self.bot.get_cog(f"PlayerCharacter-{character_thread.id}")
                _player_cogs.append(character_cog)
            self._player_cogs = _player_cogs
        return self._player_cogs

    @commands.Cog.listener(name="on_thread_create")
    async def _handle_create_character(self, thread):
        if thread.owner.id == self._player_id:
            self._player_characters.append(thread)
            # Wait for the cog to be created
            time.sleep(5)
            self._player_cogs.append(self.bot.get_cog(f"PlayerCharacter-{thread.id}"))

    @commands.Cog.listener(name="on_message")
    async def _handle_quest_message(self, message):

        # Only process messages from this character's character profile
        if (not self._player_id or not hasattr(message.channel, "owner")
                or not hasattr(message.channel.owner, "id") or
                not message.channel.owner.id == self._player_id):
            return

        pattern = (r"https://discord(?:app)?.com/channels/918112437331427358/(?P<quest_thread_url>\d+)|"
                   r"<#(?P<quest_thread_id>\d+)>")

        matches = re.findall(pattern, message.content)
        matches = [item for match in matches for item in match if item]

        quests = []
        for thread_id in matches:
            quest = await self.bot.fetch_channel(thread_id)
            if not hasattr(quest, "parent"):
                continue
            # This isn't actually a link to a quest
            if quest.parent.id not in [1290373594781716554, 1359554902451425280]:
                continue

            quests.append(quest)

        if quests:
            non_free_quests = [
                quest
                for cog in await self.player_cogs()
                for quest in cog.quests
                if quest.name != "Bonus Experience"
            ]
            num_earned_quests = len(non_free_quests)
            if num_earned_quests % 4 == 0:
                admin_user_id = 309102962234359829
                admin = self.bot.get_user(admin_user_id)
                player = self.bot.get_user(self._player_id)

                total_quests = len([quest for cog in await self.player_cogs() for quest in cog.quests])
                for i in range(int(num_earned_quests/4) - (total_quests - num_earned_quests)):
                    await admin.send(f"{player.display_name} gets a free point of experience!")

    @commands.Cog.listener(name="on_message_edit")
    async def _handle_quest_message_update(self, message_before, message_after):
        await self._handle_quest_message(message_after)

    def ask_level(self):
        """
        Wraps dynamic command so that the level for the specific profile id can be queried
        :return:
        :rtype:
        """
        @commands.command(name=f"{self._player_id}-level")
        async def dynamic_command(ctx):
            admin_user_id = 309102962234359829
            admin = self.bot.get_user(admin_user_id)

            num_quests = sum([len(cog.quests) for cog in await self.player_cogs()])
            player = self.bot.get_user(self._player_id)

            await admin.send(f"{player.display_name} has gone on {num_quests} quests.")
            for cog in await self.player_cogs():
                thread = await cog.get_character_thread()
                await admin.send(f"> {thread.name} has {len(cog.quests)} quests.")

        return dynamic_command
