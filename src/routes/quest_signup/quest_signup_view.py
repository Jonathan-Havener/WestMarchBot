import discord

from routes.quest_signup.cancel_button import CancelButton
from routes.quest_signup.character_select_button import CharacterSelectButton


class CharacterSelectionView(discord.ui.View):
    def __init__(self, quest_manager, user, message, embed):
        super().__init__(timeout=None)
        self.user = user
        self.message = message
        self.embed = embed

    @classmethod
    async def create(cls, quest_manager, characters: list, user: discord.User, message, embed):
        self = cls(quest_manager, user, message, embed)

        for character in characters:
            thread = await character.get_character_thread()
            self.add_item(CharacterSelectButton(quest_manager, character, thread.name, user, self.message, self.embed))

        # self.add_item(CancelButton(user))
        return self

