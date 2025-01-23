import unittest
import time

import discord
from discord.ext import commands

from properties.config import TOKEN, PREFIX
from routines.player_signup import PlayerSignup


class PlayerSignupCase(unittest.IsolatedAsyncioTestCase):
    bot = None

    @classmethod
    def setUpClass(cls):
        intents = discord.Intents.default()
        intents.members = True
        intents.reactions = True
        intents.messages = True
        intents.message_content = True

        PlayerSignupCase.bot = commands.Bot(command_prefix=PREFIX, intents=intents)

    def setUp(self):
        self.signup = PlayerSignup(PlayerSignupCase.bot)

    async def test_get_player_history(self):
        @PlayerSignupCase.bot.event
        async def on_ready():
            await self.signup.process()
            await PlayerSignupCase.bot.close()

        await PlayerSignupCase.bot.start(TOKEN, reconnect=True)

    async def test_get_player_quest_history(self):
        @PlayerSignupCase.bot.event
        async def on_ready():
            start_time = time.time()
            history = await self.signup.get_players_quest_history()
            runtime = time.time() - start_time
            await PlayerSignupCase.bot.close()

        await PlayerSignupCase.bot.start(TOKEN, reconnect=True)

    async def test_get_player_character(self):
        @PlayerSignupCase.bot.event
        async def on_ready():
            thread = self.signup.quest_board.threads[-2]
            characters = await self.signup.get_player_characters_from_thread(thread)
            await PlayerSignupCase.bot.close()

        await PlayerSignupCase.bot.start(TOKEN, reconnect=True)

    async def test_build_embed(self):
        @PlayerSignupCase.bot.event
        async def on_ready():
            player_quests = await self.signup.get_players_quest_history()
            thread = self.signup.quest_board.threads[1]

            messages = [message async for message in thread.history(limit=None)]
            thread_participants = set([
                message.author
                for message in messages
                if message.author != thread.owner])

            these_player_quests = {
                player: player_quests[player]
                for player in thread_participants
                if player in player_quests
                   and not player.bot
            }

            player_characters = await self.signup.get_player_characters_from_thread(thread)

            embed = self.signup.build_embed(thread, these_player_quests, player_characters)

            admin_user_id = 309102962234359829
            admin = self.bot.get_user(admin_user_id)

            await admin.send(embed=embed)

            await PlayerSignupCase.bot.close()

        await PlayerSignupCase.bot.start(TOKEN, reconnect=True)


if __name__ == '__main__':
    unittest.main()
