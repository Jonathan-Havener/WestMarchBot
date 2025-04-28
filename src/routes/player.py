import discord

from discord.ext import commands
from .player_character import PlayerCharacter


class Player(commands.Cog):
    def __init__(self, bot: commands.Bot, player_id):
        self.bot = bot
        self._player_id = player_id

        self.__cog_name__ = f"Player-{player_id}"

        self._player_cogs = []

    @property
    def _player_profile_forum(self):
        player_profiles_id = 1293034430968889477
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
            if thread.owner and thread.owner.id == self._player_id
        ]

    async def _get_player_character_cog(self, char_thread_id: str) -> (PlayerCharacter, bool):
        """

        :param char_thread_id:
        :type char_thread_id:
        :return:
        :rtype:
        """
        char_cog = self.bot.get_cog(f"PlayerCharacter-{char_thread_id}")
        created = False

        if not char_cog:
            char_cog = PlayerCharacter(self.bot, char_thread_id)
            await self.bot.add_cog(char_cog)
            created = True

        if char_cog not in self._player_cogs:
            self._player_cogs.append(char_cog)

        return char_cog, created

    async def character_cogs(self) -> list[PlayerCharacter]:
        """
        lazy loads the player's characters
        :return:
        :rtype:
        """
        if not self._player_cogs:
            for character_thread in await self._get_player_char_threads():
                character_cog, _ = await self._get_player_character_cog(character_thread.id)

        return self._player_cogs

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
        if not thread.owner.id == self._player_id:
            return

        # If the thread isn't a character thread
        player_profiles_id = 1293034430968889477
        if thread.parent.id != player_profiles_id:
            return

        char_cog = PlayerCharacter(self.bot, thread.id)
        self.bot.add_cog(char_cog)
        self._player_cogs.append(char_cog)

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

            num_quests = sum([len(await cog.quests()) for cog in await self.character_cogs()])
            player = self.bot.get_user(self._player_id)

            await admin.send(f"{player.display_name} has gone on {num_quests} quests.")
            for cog in await self.character_cogs():
                thread = await cog.get_character_thread()
                await admin.send(f"> {thread.name} has {len(await cog.quests())} quests.")

        return dynamic_command
