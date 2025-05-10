import discord


class CharacterSelectionView(discord.ui.View):
    def __init__(self, user, on_select):
        super().__init__(timeout=None)
        self.user = user
        self.on_select = on_select

    @classmethod
    async def create(cls, characters: list, user: discord.User, on_select):
        self = cls(user, on_select)

        for character in characters:
            thread = await character.get_character_thread()
            self.add_item(CharacterSelectButton(character, thread.name, user))

        self.add_item(CancelButton(user))
        return self


class CharacterSelectButton(discord.ui.Button):
    def __init__(self, character, thread_name, user):
        self.character = character
        self.user = user
        super().__init__(label=thread_name, style=discord.ButtonStyle.primary, custom_id=str(character.profile_id))

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("This selection isn't for you.", ephemeral=True)
            return

        await interaction.response.defer()
        await self.view.on_select(self.character.profile_id)
        await interaction.message.delete()


class CancelButton(discord.ui.Button):
    def __init__(self, user):
        self.user = user
        super().__init__(label="Cancel", style=discord.ButtonStyle.danger, custom_id="cancel")

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("This cancellation isn't for you.", ephemeral=True)
            return

        await interaction.message.delete()
