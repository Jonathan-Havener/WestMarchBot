import discord
from .bastion_view import BastionConstructionView
from .about_bastion_view import AboutBastionView

# SECTION_VIEWS = {
#     "about": AboutBastionView,
#     "construction": BastionConstructionView,
#     # Add other views here
# }


class NavigableBastionView(discord.ui.View):
    def __init__(self, bastion, section: str = "construction"):
        super().__init__(timeout=None)
        self.bastion = bastion
        self.owner = bastion.owner
        self.section = section

        self._add_navigation_buttons()

    def _add_navigation_buttons(self):
        nav_items = {
            "about": "About",
            "construction": "Construction",
            # Add more sections here
        }

        for section_key, label in nav_items.items():
            button = discord.ui.Button(
                label=label,
                style=discord.ButtonStyle.primary if self.section == section_key else discord.ButtonStyle.secondary,
                row=1
            )

            async def callback(interaction, section=section_key):
                await self.on_navigate(interaction, section)

            button.callback = callback
            self.add_item(button)

    async def on_navigate(self, interaction: discord.Interaction, section: str):
        await interaction.response.defer()

        view_class = SECTION_VIEWS.get(section)
        if not view_class:
            await interaction.followup.send("Unknown section", ephemeral=True)
            return

        loading_msg = await interaction.followup.send("⏳ Loading section, please wait...", ephemeral=True)

        new_view = await view_class.create(self.bastion)
        await interaction.followup.edit_message(
            message_id=interaction.message.id,
            embed=new_view.initial_embed(),
            view=new_view
        )

        try:
            await loading_msg.delete()
        except discord.NotFound:
            pass  # User already dismissed it or it expired

    def initial_embed(self) -> discord.Embed:
        return discord.Embed(title="Bastion")
