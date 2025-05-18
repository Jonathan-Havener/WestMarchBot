import os

import discord
from discord.ext import commands

from .player_character import PlayerCharacter
from .character_factory import CharacterFactory


class Player(commands.Cog):
    def __init__(self, bot: commands.Bot, player_id):
        self.bot = bot
        self.player_id = player_id
        self._character_factory = CharacterFactory(self.bot, self)

        self.__cog_name__ = f"Player-{player_id}"

        self._player_cogs = set()

    @property
    def _player_profile_forum(self):
        player_profiles_id = int(os.environ.get("PLAYER_PROFILES_ID"))
        player_profiles = self.bot.get_channel(player_profiles_id)
        return player_profiles

    async def _get_player_char_threads(self) -> list:
        """
        Gets all the character threads this player has created.

        :return:
        :rtype:
        """
        older_threads = [thread async for thread in self._player_profile_forum.archived_threads() if thread]

        return [
            thread
            for thread in self._player_profile_forum.threads + older_threads
            if thread.owner and thread.owner.id == self.player_id
        ]

    async def get_character(self, profile_id):
        character, _ = await self._character_factory.get_cog(profile_id)
        self._player_cogs.add(character)
        return character

    async def character_cogs(self) -> list[PlayerCharacter]:
        """
        lazy loads the player's characters
        :return:
        :rtype:
        """
        if not self._player_cogs:
            for character_thread in await self._get_player_char_threads():
                character_cog, was_created = await self._character_factory.get_cog(character_thread.id)
                self._player_cogs.add(character_cog)

        return self._player_cogs

    async def active_character_cogs(self) -> list[PlayerCharacter]:
        """
        lazy loads the player's characters
        :return:
        :rtype:
        """
        char_cogs = await self.character_cogs()
        active_chars = []
        for char in char_cogs:
            is_active = await char.is_active_player()
            if is_active:
                active_chars.append(char)

        return active_chars

    @commands.Cog.listener(name="on_thread_create")
    async def handle_create_character(self, thread: discord.Thread):
        """
        Creates the character cog for this player
        :param thread:
        :type thread:
        :return:
        :rtype:
        """
        # If this player didn't create the thread
        if not thread.owner.id == self.player_id:
            return

        # If the thread isn't a character thread
        if thread.parent.id != self._character_factory.player_profiles_id:
            return

        char_cog, was_created = await self._character_factory.get_cog(thread.id)
        self._player_cogs.add(char_cog)

    def ask_level(self):
        """
        Wraps dynamic command so that the level for the specific profile id can be queried
        :return:
        :rtype:
        """
        @commands.command(name=f"{self.player_id}-level")
        async def dynamic_command(ctx):
            admin = self.bot.get_user(int(os.environ.get("ADMIN_ID")))

            num_quests = sum([len(await cog.quests()) for cog in await self.character_cogs()])
            player = self.bot.get_user(self.player_id)

            await admin.send(f"{player.display_name} has gone on {num_quests} quests.")
            for cog in await self.character_cogs():
                thread = await cog.get_character_thread()
                await admin.send(f"> {thread.name} has {len(await cog.quests())} quests.")

        return dynamic_command
