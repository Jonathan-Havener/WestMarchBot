import yaml
from pathlib import Path
import sys
import asyncio
import re
from datetime import datetime, timedelta, timezone

from discord.ext import commands
import discord

from .routine import Routine


class PlayerSignup(Routine):
    def __init__(self, bot):
        self.bot = bot

    @property
    def quest_board(self):
        bot_updates_channel_id = 1290373594781716554
        return self.bot.get_channel(bot_updates_channel_id)

    async def _get_character(self, message: discord.Message) -> [None, tuple]:
        pattern = "(?P<jump_url>https://discord.com/channels/918112437331427358/(?P<character_thread>\d+))"

        match = re.search(pattern, message.clean_content)

        if match:
            character_thread = await self.bot.fetch_channel(match.group("character_thread"))
            return message.author, character_thread
        return

    async def get_player_characters_from_thread(self, thread: discord.Thread) -> dict:
        characters = {}
        async for message in thread.history(limit=None):
            character_info = await self._get_character(message)
            if not character_info:
                continue

            characters.update({character_info[0]: character_info[1]})

        return characters

    async def _get_players_from_quest(self, thread, player_quests, quest_exclusions):
        async for message in thread.history(limit=None):
            if message.author == thread.owner:
                continue

            if message.author.bot:
                continue

            if message.author not in player_quests:
                player_quests[message.author] = []

            if thread in player_quests[message.author]:
                continue

            if thread.owner not in [user for reaction in message.reactions async for user in reaction.users()]:
                continue

            # Don't include quests players have said they didn't actually attend
            if (
                    message.author.id in quest_exclusions
                    and thread.id in quest_exclusions[message.author.id]
            ):
                continue

            player_quests[message.author].append(thread)

    async def get_players_quest_history(self) -> dict:
        player_quests = {}

        # Get the quests players haven't actually been on.
        quest_exclusions_path = Path(__file__).parent.parent.parent / Path("data", "quest_exclusions.yaml")
        with open(quest_exclusions_path, "r") as file:
            quest_exclusions = yaml.safe_load(file)

        tasks = []
        # Remove the "about" thread
        for thread in self.quest_board.threads[1:]:
            tasks.append(self._get_players_from_quest(thread, player_quests, quest_exclusions))

        await asyncio.gather(*tasks)
        return player_quests

    async def get_last_bot_message(self, messages) -> [discord.Message, None]:
        bot_message = next((message
                            for message in messages
                            if message.author.bot),
                           None)

        return bot_message

    def build_embed(self, thread, these_player_quests, player_characters) -> discord.Embed:
        embed = discord.Embed(
            title=thread.name,
            description=f"{thread.owner.display_name}, here is a digest of the players interested in your quest.\n"
                        f"These are the quests the players have been on in the last month."
        )

        attending_this_quest = [
            player
            for player in these_player_quests
            if thread in these_player_quests[player]
        ]
        details = ''
        for player in attending_this_quest:
            details += f"- {player.display_name}\n"
        embed.add_field(
            name=f"**{len(attending_this_quest)} player{'s' if len(attending_this_quest) > 1 else ''} "
                 f"are attending this quest!**",
            value=details,
            inline=False
        )

        other_quest_history = {
            player: [
                quest
                for quest in these_player_quests[player]
                if quest != thread
            ]
            for player in these_player_quests
        }

        for count, player in enumerate(other_quest_history):
            details = ''
            for quest in other_quest_history[player]:
                details += f"- {quest.jump_url}\n"
            embed.add_field(
                name=f"**{player.display_name}** - {len(other_quest_history[player])} quests{' (Waitlist?)' if count > 4 else ''}",
                value=details,
                inline=False
            )

        return embed

    async def process(self):
        player_quests = await self.get_players_quest_history()

        for thread in self.quest_board.threads[::-1]:
            if thread.created_at < (datetime.now() - timedelta(days=5)).replace(tzinfo=timezone.utc):
                break

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

            these_player_quests = dict(sorted(these_player_quests.items(), key=lambda item: len(item[1])))

            player_characters = await self.get_player_characters_from_thread(thread)

            embed = self.build_embed(thread, these_player_quests, player_characters)

            bot_message = await self.get_last_bot_message(messages)
            if bot_message:
                await bot_message.edit(embed=embed)
            else:
                await thread.send(embed=embed)
