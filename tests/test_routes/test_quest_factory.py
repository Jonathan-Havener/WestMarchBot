import unittest

import discord
from discord.ext import commands

from properties.config import PREFIX
from routes.quest_factory import QuestFactory


class QuestFactoryCase(unittest.IsolatedAsyncioTestCase):
    bot = None

    @classmethod
    def setUpClass(cls):
        intents = discord.Intents.default()
        intents.members = True
        intents.reactions = True
        intents.messages = True
        intents.message_content = True

        QuestFactoryCase.bot = commands.Bot(command_prefix=PREFIX, intents=intents)

    def setUp(self):
        self.q_factory = QuestFactory(QuestFactoryCase.bot)

    def test_on_message(self):
        listeners = self.q_factory.get_listeners()
        print(listeners)
