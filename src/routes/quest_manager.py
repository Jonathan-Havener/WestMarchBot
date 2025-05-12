import os
import re
import logging

from discord.ext import commands
import discord

from .player_factory import PlayerFactory
from .quest_signup.quest_thread_view import QuestThreadView
from .quest_signup.character_select_button import JoinRequestView


class QuestManager(commands.Cog):
    def __init__(self, bot: commands.Bot, quest_id, player_factory: PlayerFactory):
        self.bot = bot
        self._quest_id = quest_id
        self._quest_thread = None
        self.player_factory = player_factory

        self.approved_users = set()
        self.waitlisted_users = set()

        self._adventurers = set()
        self._message_responses = []
        self._bot_message = None

        self._setup_subscriptions()

        self.__cog_name__ = f"Quest-{quest_id}"

        self._queried_players = set([])

    @classmethod
    async def create(cls, bot: commands.Bot, quest_id, player_factory: PlayerFactory):
        self = cls(bot, quest_id, player_factory)

        quest_thread = await self.get_quest_thread()

        bot_message = await self.bot_message()
        if bot_message:
            embed = bot_message.embeds[0]

            approved_text = next((field.value for field in embed.fields if "Approved" in field.name), "")
            mentioned_characters = self._get_character_threads_from_message(approved_text)
            for thread_id in mentioned_characters:
                await self._add_adventurer(self.approved_users, thread_id)

            waitlisted_text = next((field.value for field in embed.fields if "Waitlisted" in field.name), "")
            mentioned_characters = self._get_character_threads_from_message(waitlisted_text)
            for thread_id in mentioned_characters:
                await self._add_adventurer(self.waitlisted_users, thread_id)

            # Recreate the view with existing data
            view = QuestThreadView(self, quest_thread.owner, bot_message, embed)
            await bot_message.edit(embed=embed, view=view)
            self._bot_message = bot_message
        else:
            embed = await self.build_embed(quest_thread)
            message = await quest_thread.send(embed=embed)
            view = QuestThreadView(self, quest_thread.owner, message, embed)
            self._bot_message = await message.edit(embed=embed, view=view)

        logging.info(f"Created new quest thread for quest ID {quest_id}: {quest_thread.name} (ID: {quest_thread.id})")

        await self.relink_join_request_views()

        return self

    async def relink_join_request_views(self):
        messages = [message async for message in self._quest_thread.history(limit=None)]
        for message in messages:
            if "joined the frey!" in message.content:
                bot_message = await self.bot_message()

                match = re.search(r"<@(\d+)>", message.content)
                if not match:
                    return
                user_id = match.group(1)
                player_cog, player_was_created = await self.player_factory.get_cog(user_id)

                character_thread_id = self._get_character_threads_from_message(message.content)[0]
                # Creates the character if it didn't already exist
                char_cog = await player_cog.get_character(character_thread_id)

                view = JoinRequestView(self, self._quest_thread.owner, char_cog, bot_message, bot_message.embeds[0])
                message = await message.edit(content = message.content, view=view)

    async def get_quest_thread(self):
        if self._quest_thread:
            return self._quest_thread

        self._quest_thread = await self.bot.fetch_channel(self._quest_id)
        return self._quest_thread

    async def _add_adventurer(self, approval_set, character_thread_id: int):
        character = await self.bot.fetch_channel(character_thread_id)
        if not hasattr(character, "parent"):
            return
        if character.parent.id != int(os.environ.get("PLAYER_PROFILES_ID")):
            return
        if character in self._adventurers:
            return

        player_cog, player_was_created = await self.player_factory.get_cog(character.owner.id)
        # Creates the character if it didn't already exist
        char_cog = await player_cog.get_character(character_thread_id)

        approval_set.add(char_cog)

    def _get_character_threads_from_message(self, text) -> list[int]:
        pattern = (fr"https://discord(?:app)?.com/channels/{os.environ.get('SERVER_ID')}/(?P<character_thread_url>\d+)|"
                   r"<#(?P<character_thread_id>\d+)>")

        matches = re.findall(pattern, text)
        matches = [item for match in matches for item in match if item]
        return matches

    async def bot_message(self):
        if self._bot_message:
            return self._bot_message
        messages = [message async for message in self._quest_thread.history(limit=None)]
        self._bot_message = await self.get_adventurer_list_message(messages)
        return self._bot_message

    def _setup_subscriptions(self):
        """
        This initializes all the responses we may have for a message
        This is primarily used when processing a history of messages sent before the cog was created
        :return:
        :rtype:
        """
        pass
        # self._message_responses.append(self._handle_signup_message)

    async def get_adventurer_list_message(self, messages) -> [discord.Message, None]:
        bot_message = next((message
                            for message in messages
                            if message.author.bot and message.embeds and
                            "players interested" in message.embeds[0].description),
                           None)

        return bot_message

    async def build_embed(self, thread) -> discord.Embed:
        embed = discord.Embed(
            title=thread.name,
            description=f"{thread.owner.display_name}, here is a digest of the players interested in your quest."
        )

        details = ''
        for adventurer in self._adventurers:
            character_thread = await adventurer.get_character_thread()
            url = character_thread.jump_url

            character_tags = [
                tag.name
                for tag in character_thread.applied_tags
                if tag.name != 'Player Character'
            ]
            character_tag_text = f"{'/'.join(character_tags)}"

            character_text = f"as {url}. Level - {await adventurer.level()} {character_tag_text}"
            details += f"- {character_thread.owner.display_name} {character_text}\n"
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

    # async def _send_character_selection_message(self, player: discord.User, player_characters):
    #     quest_thread = await self.get_quest_thread()
    #     emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
    #
    #     message_content = ""
    #
    #     timed_characters = {}
    #     for character in player_characters:
    #         char_thread = await character.get_character_thread()
    #
    #         non_player_tags = ["NPC", "Deceased", "pregen"]
    #         actual_tags = [tag.name for tag in char_thread.applied_tags]
    #         # Ignore this character if it has any of these tags
    #         if not actual_tags or not set(non_player_tags).isdisjoint(set(actual_tags)):
    #             continue
    #
    #         last_message = next(iter([msg async for msg in char_thread.history(limit=1)]), None)
    #         if not last_message:
    #             continue
    #         last_message_time = last_message.edited_at or last_message.created_at
    #         timed_characters.update({last_message_time: character})
    #
    #     recent_characters = [timed_characters[k] for k in sorted(timed_characters.keys(), reverse=True)]
    #
    #     for index, character_cog in enumerate(recent_characters[:len(emojis)]):
    #         char_thread = await character_cog.get_character_thread()
    #         message_content += (
    #             f"{index+1} : "
    #             f"[{char_thread.name}]"
    #             f"({char_thread.jump_url}) "
    #             f"Level {await character_cog.level()} "
    #         )
    #         character_tags = [
    #             tag.name
    #             for tag in char_thread.applied_tags
    #             if tag.name != 'Player Character'
    #         ]
    #         message_content += "/".join(character_tags)
    #         message_content += "\n"
    #
    #     message_content = f"{player.mention}, who would you like to play?\n" + message_content
    #
    #     player_req_msg = await quest_thread.send(f"{quest_thread.name}\n{message_content}")
    #     for idx, player_option in enumerate(recent_characters[:len(emojis)]):
    #         await player_req_msg.add_reaction(emojis[idx])
    #
    #     await player_req_msg.add_reaction("❌")

    # @commands.Cog.listener(name="on_message")
    # async def _handle_signup_message(self, message):
    #
    #     # Only process messages from this quest thread
    #     if not self._quest_id or not message.channel.id == self._quest_id:
    #         return
    #
    #     if message.author.bot:
    #         return
    #
    #     mentioned_characters = self._get_character_threads_from_message(message)
    #
    #     for thread_id in mentioned_characters:
    #         await self._add_adventurer(thread_id)
    #
    #     if mentioned_characters:
    #         quest_thread = await self.get_quest_thread()
    #         # Update the embed
    #         embed = await self.build_embed(quest_thread)
    #         bot_message = await self.bot_message()
    #         if bot_message:
    #             await bot_message.edit(embed=embed)
    #         else:
    #             await quest_thread.send(embed=embed)
    #
    # @commands.Cog.listener(name="on_message_edit")
    # async def _handle_signup_message_update(self, message_before, message_after):
    #     await self._handle_signup_message(message_after)
