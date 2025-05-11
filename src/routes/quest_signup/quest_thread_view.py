import discord

from discord import ui, ButtonStyle, Interaction
from routes.quest_signup.quest_signup_view import CharacterSelectionView


class QuestThreadView(ui.View):
    def __init__(self, quest_manager: "QuestManager", thread_owner: discord.User, message, embed):
        super().__init__(timeout=None)
        self.quest_manager = quest_manager
        self.thread_owner = thread_owner

        self.message = message
        self.embed = embed

        self.add_item(SignupButton(quest_manager, self.message, self.embed))
        self.add_item(AwardXPButton(quest_manager, thread_owner))


class SignupButton(ui.Button):
    def __init__(self, quest_manager: "QuestManager", message, embed):
        super().__init__(label="Signup", style=ButtonStyle.primary)
        self.quest_manager = quest_manager
        self.message = message
        self.embed = embed

    async def callback(self, interaction: Interaction):
        player_cog, _ = await self.quest_manager.player_factory.get_cog(interaction.user.id)
        player_characters = await player_cog.character_cogs()

        embed = discord.Embed(
            title="Who would you like to play?",
            description="Choose one of your characters below:",
            color=discord.Color.green()
        )

        view = await CharacterSelectionView.create(
            self.quest_manager, player_characters, interaction.user, self.message, self.embed
        )
        await interaction.response.send_message(content=interaction.user.mention, embed=embed, view=view, ephemeral=True)


class AwardXPButton(ui.Button):
    def __init__(self, quest_manager: "QuestManager", thread_owner: discord.User):
        super().__init__(label="Award Experience", style=ButtonStyle.success)
        self.quest_manager = quest_manager
        self.thread_owner = thread_owner

    async def callback(self, interaction: Interaction):
        if interaction.user != self.thread_owner:
            await interaction.response.send_message("Only the quest creator can award experience.", ephemeral=True)
            return

        await interaction.response.send_message("✅ Experience awarded! (This is a placeholder)", ephemeral=True)
