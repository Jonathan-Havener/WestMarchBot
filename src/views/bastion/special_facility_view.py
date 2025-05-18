import discord

from logic.bastion.choice import Choice
from views.bastion.choice_embed import ChoiceEmbed
from views.bastion.special_facility_info_embed import SpecialFacilityInfoEmbed


class SpecialFacilityView(discord.ui.View):
    def __init__(self, facility, owner):
        super().__init__(timeout=None)
        self.facility = facility
        self.owner = owner
        self.main_view = None
        self.selected_choice = "info"  # Track as string or actual choice
        self.choice_buttons = {}       # choice -> button
        self.info_view_btn = None      # Will hold reference to Info View button

    @classmethod
    async def create(cls, facility, owner):
        self = cls(facility, owner)
        self.main_view = await SpecialFacilityInfoEmbed.create(facility, owner)

        # Add Info View button manually (so we can track it)
        info_btn = discord.ui.Button(label="Info View", style=discord.ButtonStyle.primary)

        async def info_callback(interaction: discord.Interaction):
            self.selected_choice = "info"
            await self._update_button_styles()
            await interaction.response.edit_message(embed=self.main_view, view=self)

        info_btn.callback = info_callback
        self.info_view_btn = info_btn
        self.add_item(info_btn)

        # Add dynamic choice buttons
        for choice in self.facility.choices:
            button = self._make_choice_button(choice)
            self.choice_buttons[choice] = button
            self.add_item(button)

        # Set initial style
        await self._update_button_styles()
        return self

    def _make_choice_button(self, choice: "Choice") -> discord.ui.Button:
        button = discord.ui.Button(label=choice.name, style=discord.ButtonStyle.secondary)

        async def callback(interaction: discord.Interaction):
            self.selected_choice = choice
            await self._update_button_styles()

            choice_embed = await ChoiceEmbed.create(self.facility, self.owner, choice)
            await interaction.response.edit_message(embed=choice_embed, view=self)

        button.callback = callback
        return button

    async def _update_button_styles(self):
        # Update info view button style
        if self.info_view_btn:
            self.info_view_btn.style = (
                discord.ButtonStyle.primary if self.selected_choice == "info"
                else discord.ButtonStyle.secondary
            )

        # Update each choice button
        for choice, button in self.choice_buttons.items():
            button.style = (
                discord.ButtonStyle.primary if choice == self.selected_choice
                else discord.ButtonStyle.secondary
            )
