import re

from discord.ext import commands
import discord


class PlayerCharacter(commands.Cog):
    def __init__(self, bot, profile_id):
        self.bot = bot
        self._profile_id = profile_id
        self._character_thread = None

        self._quests = []
        self._message_responses = []

        self._last_message = None

        self.__cog_name__ = f"PlayerCharacter-{profile_id}"

        self.bot.add_command(self.ask_level())

    async def _get_quests_from_msg(self, message) -> list[discord.Thread]:
        """

        :param message:
        :type message:
        :return:
        :rtype:
        """
        quests = []

        pattern = (r"https://discord(?:app)?.com/channels/918112437331427358/(?P<quest_thread_url>\d+)|"
                   r"<#(?P<quest_thread_id>\d+)>")

        matches = re.findall(pattern, message.content)
        matches = [item for match in matches for item in match if item]

        for thread_id in matches:
            try:
                quest: discord.Thread = await self.bot.fetch_channel(thread_id)
            except discord.errors.NotFound:
                print(f"Quest not found in message.\n{message.content}")
                continue
            except Exception as e:
                print(f"Encountered an unknown error looking for quest in msg.\n{message.content}")
                continue

            if not hasattr(quest, "parent"):
                continue
            if quest.parent.id not in [1290373594781716554, 1359554902451425280]:
                continue

            quests.append(quest)

        return quests

    async def quests(self) -> list:
        """
        # TODO: need to search history when this is called
        :return:
        :rtype:
        """
        if not self._quests:
            await self._populate_quest_history()

        return self._quests

    async def _populate_quest_history(self) -> None:
        this_thread = await self.get_character_thread()
        async for message in this_thread.history(limit=None):
            quests = await self._get_quests_from_msg(message)
            for quest in quests:
                if quest in self._quests:
                    continue
                self._quests.append(quest)

    async def _add_quest(self, quest: discord.Thread) -> None:
        this_thread = await self.get_character_thread()

        # Make sure we've initialized the quest from history before we add one
        if not self._quests:
            await self._populate_quest_history()

        level_before = await self.level()
        self._quests.append(quest)
        level_after = await self.level()

        if level_after != level_before:
            await this_thread.send(f"{this_thread.name} hit level {self.level}! Congrats :)")

    async def level(self) -> int:
        return 3 + int(len(await self.quests()) / 4)

    async def get_character_thread(self) -> discord.Thread:
        if not self._character_thread:
            self._character_thread = await self.bot.fetch_channel(self._profile_id)

        return self._character_thread

    @commands.Cog.listener(name="on_message")
    async def handle_quest_message(self, message):

        # Only process messages from this character's character profile
        if not self._profile_id or not message.channel.id == self._profile_id:
            return

        quests = await self._get_quests_from_msg(message)
        for quest in quests:
            if quest in self._quests:
                continue
            await self._add_quest(quest)

    @commands.Cog.listener(name="on_message_edit")
    async def _handle_quest_message_update(self, message_before, message_after):
        await self.handle_quest_message(message_after)

    def ask_level(self):
        """
        Wraps dynamic command so that the level for the specific profile id can be queried
        :return:
        :rtype:
        """

        @commands.command(name=f"{self._profile_id}-level")
        async def dynamic_command(ctx):
            admin_user_id = 309102962234359829
            admin = self.bot.get_user(admin_user_id)
            this_thread = await self.get_character_thread()

            await admin.send(f"{this_thread.jump_url} by {this_thread.owner.display_name} is level {self.level}")

        return dynamic_command
