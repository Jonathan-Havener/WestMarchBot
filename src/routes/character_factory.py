import os
import asyncio

import discord
from discord.ext import commands
from .player_character import PlayerCharacter


class CharacterFactory(commands.Cog):
    def __init__(self, bot: commands.Bot, player_cog):
        self.bot = bot
        self.player_cog = player_cog

        self.player_profiles_id = int(os.environ.get("PLAYER_PROFILES_ID"))
        self._locks = {}

    def _get_lock(self, quest_id: str) -> asyncio.Lock:
        return self._locks.setdefault(quest_id, asyncio.Lock())

    async def get_cog(self, profile_id: int):
        profile_id = int(profile_id)
        lock = self._get_lock(profile_id)
        async with lock:

            character_cog = self.bot.get_cog(f"PlayerCharacter-{profile_id}")
            created = False

            if not character_cog:
                character_cog = await PlayerCharacter.create(self.bot, int(profile_id), self.player_cog)
                await self.bot.add_cog(character_cog)
                created = True

            return character_cog, created
