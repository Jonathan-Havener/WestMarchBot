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
