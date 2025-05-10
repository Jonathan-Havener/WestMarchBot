import os
import yaml
from pathlib import Path
import asyncio
import re
from datetime import datetime, timedelta, timezone

import discord

from .routine import Routine


class PlayerSignup(Routine):
    def __init__(self, bot):
        self.bot = bot

    @property
    def quest_board(self):
        return self.bot.get_channel(int(os.environ.get("QUEST_BOARD_ID")))

    @property
    def request_board(self):
        return self.bot.get_channel(int(os.environ.get("REQUEST_BOARD_ID")))

    async def _get_character(self, message: discord.Message, character_info) -> None:
        link_pattern = fr"(?P<jump_url>https://discord(?:app)?.com/channels/{os.environ.get('SERVER_ID')}/(?P<character_thread>\d+))"
        id_pattern = r"<#(?P<character_thread>\d+)>"

        match = re.search(link_pattern, message.content) or re.search(id_pattern, message.content)

        if match:
            character_thread = await self.bot.fetch_channel(match.group("character_thread"))
            character_info.update({message.author: character_thread})

    async def get_player_characters_from_thread(self, thread: discord.Thread) -> dict:
        characters = {}
        async for message in thread.history(limit=None):
            await self._get_character(message, characters)

        return characters

    async def _get_players_from_quest(self, quest_thread, player_quests, quest_exclusions):
        async for message in quest_thread.history(limit=None):
            if message.author == quest_thread.owner:
                continue

            if message.author.bot:
                continue

            if message.author not in player_quests:
                player_quests[message.author] = []

            if quest_thread in player_quests[message.author]:
                continue

            if quest_thread.owner not in [user for reaction in message.reactions async for user in reaction.users()]:
                continue

            # Don't include quests players have said they didn't actually attend
            if (
                    message.author.id in quest_exclusions
                    and quest_thread.id in quest_exclusions[message.author.id]
            ):
                continue

            player_quests[message.author].append(quest_thread)

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
            character_text = f" as {player_characters[player].jump_url}" if player in player_characters else ""
            details += f"- {player.display_name}{character_text}\n"
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

        for thread in self.quest_board.threads[::-1] + self.request_board.threads[::-1]:
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
