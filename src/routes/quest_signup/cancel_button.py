import discord


class CancelButton(discord.ui.Button):
    def __init__(self, user):
        self.user = user
        super().__init__(label="Cancel", style=discord.ButtonStyle.danger, custom_id="cancel")

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("This cancellation isn't for you.", ephemeral=True)
            return

        await interaction.message.delete()
