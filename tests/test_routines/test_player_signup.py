import unittest

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

    async def test_something(self):
        signup = PlayerSignup(PlayerSignupCase.bot)

        @PlayerSignupCase.bot.event
        async def on_ready():
            await signup.process()
            await PlayerSignupCase.bot.close()

        await PlayerSignupCase.bot.start(TOKEN)


if __name__ == '__main__':
    unittest.main()
