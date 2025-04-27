from discord.ext import commands
import discord
import re
from .player_character import PlayerCharacter


class QuestManager(commands.Cog):
    def __init__(self, bot: commands.Bot, quest_id):
        self.bot = bot
        self._quest_id = quest_id
        self._quest_thread = None

        self._adventurers = []
        self._message_responses = []
        self._bot_message = None

        self._setup_subscriptions()

        self.__cog_name__ = f"Quest-{quest_id}"

        self._queried_players = []

        # self.bot.add_command(self.ask_level())

    async def get_quest_thread(self):
        if self._quest_thread:
            return self._quest_thread

        self._quest_thread = await self.bot.fetch_channel(self._quest_id)
        return self._quest_thread

    async def _add_adventurer(self, character_thread_id, character):
        self._adventurers.append(character)
        player_cog = self.bot.get_cog(f"PlayerCharacter-{character_thread_id}")
        if not player_cog:
            player_cog = PlayerCharacter(self.bot, character_thread_id)
            await self.bot.add_cog(player_cog)

    async def bot_message(self):
        if self._bot_message:
            return self._bot_message
        messages = [message async for message in self._quest_thread.history(limit=None)]
        self._bot_message = await self.get_last_bot_message(messages)
        return self._bot_message

    @commands.Cog.listener(name="on_reaction_add")
    async def on_reaction_add(self, reaction, user):
        if not self._quest_id or not reaction.message.channel.id == self._quest_id:
            return
        if user.bot:
            return
        if not reaction.message.author.bot:
            return
        if "who would you like to play?" not in reaction.message.content:
            return
        if user.mention not in reaction.message.content:
            return

        if reaction.emoji == "❌":
            await reaction.message.delete()

        emoji_map = {'1️⃣':1, '2️⃣':2, '3️⃣':3, '4️⃣':4, '5️⃣':5}
        lines = reaction.message.content.split("\n")
        selection = next(line for line in lines[2:] if str(emoji_map[reaction.emoji]) in line.split(":")[0])

        thread_id = selection.split(")")[0].split("/")[-1]
        character = await self.bot.fetch_channel(thread_id)

        await self._add_adventurer(thread_id, character)

        quest_thread = await self.get_quest_thread()
        # Update the embed
        embed = self.build_embed(quest_thread)
        bot_message = await self.bot_message()
        if bot_message:
            await bot_message.edit(embed=embed)
        else:
            await quest_thread.send(embed=embed)

        await reaction.message.delete()

    @commands.Cog.listener(name="on_message")
    async def _handle_nosignup_message(self, message):
        # Only process messages from this quest thread
        if not self._quest_id or not message.channel.id == self._quest_id:
            return

        if message.author.id in self._queried_players:
            return

        quest_thread = await self.get_quest_thread()
        if message.author == quest_thread.owner:
            return

        pattern = (r"https://discord(?:app)?.com/channels/918112437331427358/(?P<character_thread_url>\d+)|"
                   r"<#(?P<character_thread_id>\d+)>")

        matches = re.findall(pattern, message.content)
        matches = [item for match in matches for item in match if item]

        if matches:
            return

        # Player has already sent a character in this thread
        if message.author.id in [character.owner.id for character in self._adventurers]:
            return

        player_cog = self.bot.get_cog(f"Player-{message.author.id}")

        # Author doesn't have a character
        if not player_cog:
            return

        player_characters = await player_cog.player_cogs()

        if not player_characters:
            return

        emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

        message_content = ""

        for index, character_cog in enumerate(player_characters):
            char_thread = await character_cog.get_character_thread()
            message_content += (
                f"{index+1} : "
                f"[{char_thread.name}]"
                f"({char_thread.jump_url}) "
                f"Level {character_cog.level} "
            )
            character_tags = [
                tag.name
                for tag in char_thread.applied_tags
                if tag.name != 'Player Character'
            ]
            message_content += "/".join(character_tags)
            message_content += "\n"

        message_content = f"{message.author.mention}, who would you like to play?\n" + message_content

        player_req_msg = await quest_thread.send(f"{quest_thread.name}\n{message_content}")
        for idx, player_option in enumerate(player_characters[:5]):
            await player_req_msg.add_reaction(emojis[idx])

        await player_req_msg.add_reaction("❌")

        self._queried_players.append(message.author.id)

    @commands.Cog.listener(name="on_message")
    async def _handle_signup_message(self, message):

        # Only process messages from this quest thread
        if not self._quest_id or not message.channel.id == self._quest_id:
            return

        if message.author.bot:
            return

        pattern = (r"https://discord(?:app)?.com/channels/918112437331427358/(?P<character_thread_url>\d+)|"
                   r"<#(?P<character_thread_id>\d+)>")

        matches = re.findall(pattern, message.content)
        matches = [item for match in matches for item in match if item]

        for thread_id in matches:
            character = await self.bot.fetch_channel(thread_id)
            if not hasattr(character, "parent"):
                continue
            if character.parent.id != 1293034430968889477:
                continue
            if character in self._adventurers:
                continue
            await self._add_adventurer(thread_id, character)

        if matches:
            quest_thread = await self.get_quest_thread()
            # Update the embed
            embed = self.build_embed(quest_thread)
            bot_message = await self.bot_message()
            if bot_message:
                await bot_message.edit(embed=embed)
            else:
                await quest_thread.send(embed=embed)

    @commands.Cog.listener(name="on_message_edit")
    async def _handle_signup_message_update(self, message_before, message_after):
        await self._handle_signup_message(message_after)

    def _setup_subscriptions(self):
        """
        This initializes all the responses we may have for a message
        This is primarily used when processing a history of messages sent before the cog was created
        :return:
        :rtype:
        """
        self._message_responses.append(self._handle_signup_message)

    async def get_last_bot_message(self, messages) -> [discord.Message, None]:
        bot_message = next((message
                            for message in messages
                            if message.author.bot and message.embeds),
                           None)

        return bot_message

    def build_embed(self, thread) -> discord.Embed:
        embed = discord.Embed(
            title=thread.name,
            description=f"{thread.owner.display_name}, here is a digest of the players interested in your quest."
        )

        details = ''
        for player in self._adventurers:
            player_cog = self.bot.get_cog(f"PlayerCharacter-{player.id}")

            character_text = (f"as {player.jump_url}. Level - {player_cog.level} "
                              f"{'/'.join([tag.name for tag in player.applied_tags if tag.name != 'Player Character'])}")
            details += f"- {player.owner.display_name} {character_text}\n"
        embed.add_field(
            name=f"**{len(self._adventurers)} player{'s' if len(self._adventurers) > 1 else ''} "
                 f"are interested in this quest!**",
            value=details,
            inline=False
        )

        return embed

    async def process_history(self):
        this_thread = await self.get_quest_thread()
        print(f"Processing quest history for {this_thread.owner.display_name}'s quest {this_thread.name}")
        messages = [message async for message in this_thread.history(limit=None)]
        for message in messages:
            await self.process_message(message)

    async def process_message(self, message):
        """
        This invokes all the on_message methods as if the message was just sent.
        This is used to process history.
        """
        for callback in self._message_responses:
            await callback(message)
