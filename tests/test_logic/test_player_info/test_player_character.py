import unittest
import asyncio

from routes.player_character import PlayerCharacter
from properties.config import TOKEN, PREFIX

import discord
from discord.ext import commands


class PlayerCharacterTestCase(unittest.IsolatedAsyncioTestCase):
    bot = None
    ready_event = asyncio.Event()

    @classmethod
    def setUpClass(cls):
        intents = discord.Intents.default()
        intents.members = True
        intents.reactions = True
        intents.messages = True
        intents.message_content = True

        PlayerCharacterTestCase.bot = commands.Bot(command_prefix=PREFIX, intents=intents)
        cls.bot_task = None

    async def asyncSetUp(self):
        """Set up test case."""
        if not self.bot_task:  # Start the bot only once
            await self.start_bot()
        ming_id = 1307781750772072599
        self.jorden_ming = PlayerCharacter(self.bot, ming_id)
        await self.jorden_ming.process_history()

    async def asyncTearDown(self):
        """Tear down test case."""
        await self.stop_bot()

    @classmethod
    async def start_bot(cls):
        """Start the bot asynchronously in a separate task."""

        @PlayerCharacterTestCase.bot.event
        async def on_ready():
            print(f'Logged in as {cls.bot.user}')
            cls.ready_event.set()  # Set the event when the bot is ready

        cls.bot_task = asyncio.create_task(cls.bot.start(TOKEN, reconnect=True))

        await cls.ready_event.wait()

    @classmethod
    async def stop_bot(cls):
        """Stop the bot and ensure the task is cleaned up."""
        if cls.bot.is_closed():
            return

        # Gracefully close the bot
        await cls.bot.close()

        # Cancel the bot task if it's still running
        if cls.bot_task and not cls.bot_task.done():
            cls.bot_task.cancel()
            try:
                await cls.bot_task
            except asyncio.CancelledError:
                pass

    async def test_get_character_quests(self):
        quests = self.jorden_ming.quests
        self.jorden_ming.level
        print(quests)


if __name__ == '__main__':
    unittest.main()
