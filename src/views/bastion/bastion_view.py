import discord
from views.bastion.special_facility_info_embed import SpecialFacilityInfoEmbed
from views.bastion.special_facility_view import SpecialFacilityView


class BastionView(discord.ui.View):
    def __init__(self, bastion):
        super().__init__(timeout=None)
        self.bastion = bastion
        self.owner = bastion.owner

        self.selected_facility = None
        self.facility_buttons = {}
        self.embeds = {}
        self.add_button = None

    @classmethod
    async def create(cls, bastion):
        self = cls(bastion)

        await self._add_facility_selection_buttons()

        return self

    async def _add_facility_selection_buttons(self):
        available_facilities = await self.bastion.get_available_facilities()

        if not available_facilities:
            return self  # No facilities to show

        # Set default selected facility
        self.selected_facility = next(iter(available_facilities))

        # Preload embeds for each facility
        for facility in iter(available_facilities):
            embed = await SpecialFacilityInfoEmbed.create(facility, self.owner)
            self.embeds[facility] = embed

            button = self._make_facility_button(facility)
            self.facility_buttons[facility] = button
            self.add_item(button)

        # Add "+ Add Facility" button
        self.add_button = discord.ui.Button(label="+ Add Facility", style=discord.ButtonStyle.success)

        self.add_button.callback = self.add_callback
        self.add_item(self.add_button)

        await self._update_button_styles()

    async def add_callback(self, interaction: discord.Interaction):
        view = await SpecialFacilityView.create(self.selected_facility, self.bastion.owner)
        await interaction.response.send_message(embed=view.main_view, view=view)

    def _make_facility_button(self, facility):
        button = discord.ui.Button(label=facility.name, style=discord.ButtonStyle.secondary)

        async def callback(interaction: discord.Interaction):
            self.selected_facility = facility
            await self._update_button_styles()

            embed = self.embeds.get(facility)
            if embed:
                await interaction.response.edit_message(embed=embed, view=self)

        button.callback = callback
        return button

    async def _update_button_styles(self):
        for facility, button in self.facility_buttons.items():
            button.style = (
                discord.ButtonStyle.primary
                if facility == self.selected_facility
                else discord.ButtonStyle.secondary
            )
