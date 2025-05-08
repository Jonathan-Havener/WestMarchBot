import discord
from discord.ext import commands
from .player_character import PlayerCharacter


class CharacterFactory(commands.Cog):
    def __init__(self, bot: commands.Bot, player_cog):
        self.bot = bot
        self.player_cog = player_cog

        self.player_profiles_id = 1293034430968889477

    async def get_cog(self, profile_id: str):
        character_cog = self.bot.get_cog(f"PlayerCharacter-{profile_id}")
        created = False

        if not character_cog:
            character_cog = PlayerCharacter(self.bot, profile_id, self.player_cog)
            await self.bot.add_cog(character_cog)
            created = True

        return character_cog, created

    # @commands.Cog.listener(name="on_thread_create")
    # async def _quest_created(self, thread: discord.Thread):
    #     """
    #     Creates a quest manager cog and adds it to the bot when a quest is created
    #     :param thread:
    #     :type thread:
    #     :return:
    #     :rtype:
    #     """
    #     if not thread.channel.parent or thread.channel.parent.id not in self._quest_forums:
    #         return
    #
    #     _, _ = await self.get_cog(thread.id)
    #
    # @commands.Cog.listener(name="on_message")
    # async def _quest_message(self, message: discord.Message):
    #     """
    #     Create a quest manager cog when someone sends a message into quest channel that doesn't already have
    #     a cog
    #     :param message:
    #     :type message:
    #     :return:
    #     :rtype:
    #     """
    #     if message.channel.parent.id not in self._quest_forums:
    #         return
    #
    #     quest_cog, is_new = await self.get_cog(message.channel.id)
    #
    #     if not is_new:
    #         return
    #
    #     # Pass the message along to the created quest manager
    #     for listener in quest_cog.get_listeners():
    #         key, method = listener
    #
    #         if key != "on_message":
    #             continue
    #
    #         await method(message)
    #
    #     await quest_cog.process_history()
