import discord

from views.bastion.about_bastion_view import AboutBastionView
from views.bastion.navigable_bastion_view import NavigableBastionView
from views.bastion.special_facility_info_embed import SpecialFacilityInfoEmbed
from views.bastion.special_facility_view import SpecialFacilityView


class BastionConstructionView(NavigableBastionView):
    def __init__(self, bastion):
        super().__init__(bastion, section="construction")
        self.selected_facility = None
        self.facility_buttons = {}
        self.embeds = {}
        self.add_button = None
        self.left_index = 0
        self.facilities = []

    @classmethod
    async def create(cls, bastion):
        self = cls(bastion)
        facilities = sorted(await self.bastion.get_available_facilities(), key=lambda f: f.name)
        if facilities:
            self.selected_facility = facilities[0]
            for facility in facilities:
                embed = await SpecialFacilityInfoEmbed.create(facility, self.owner)
                self.embeds[facility] = embed

        await self._render_carousel_page()
        await self._update_button_styles()

        # Add "+ Add Facility" button on its own row
        self.add_button = discord.ui.Button(label="+ Add Facility", style=discord.ButtonStyle.success, row=3)
        self.add_button.callback = self.add_callback
        self.add_item(self.add_button)

        return self

    async def _render_carousel_page(self):
        # Remove buttons that are on row 2
        for item in list(self.children):  # Make a copy to avoid modifying the list during iteration
            if isinstance(item, discord.ui.Button) and getattr(item, 'row', None) == 2:
                self.remove_item(item)

        facilities = sorted(await self.bastion.get_available_facilities(), key=lambda f: f.name)

        if len(facilities) <= 5:
            for facility in facilities:
                button = self._make_facility_button(facility)
                self.facility_buttons[facility] = button
                self.add_item(button)
            return

        if self.left_index == 0:
            for facility in facilities[0:4]:
                button = self._make_facility_button(facility)
                self.facility_buttons[facility] = button
                self.add_item(button)
            right_button = discord.ui.Button(label="→", style=discord.ButtonStyle.secondary, row=2)
            right_button.callback = self._page_right
            self.add_item(right_button)
        elif len(facilities) - self.left_index <= 4:
            left_button = discord.ui.Button(label="←", style=discord.ButtonStyle.secondary, row=2)
            left_button.callback = self._page_left
            self.add_item(left_button)
            for facility in facilities[self.left_index::]:
                button = self._make_facility_button(facility)
                self.facility_buttons[facility] = button
                self.add_item(button)
        else:
            left_button = discord.ui.Button(label="←", style=discord.ButtonStyle.secondary, row=2)
            left_button.callback = self._page_left
            self.add_item(left_button)
            for facility in facilities[self.left_index:self.left_index+3]:
                button = self._make_facility_button(facility)
                self.facility_buttons[facility] = button
                self.add_item(button)
            right_button = discord.ui.Button(label="→", style=discord.ButtonStyle.secondary, row=2)
            right_button.callback = self._page_right
            self.add_item(right_button)

    def _make_facility_button(self, facility):
        button = discord.ui.Button(label=facility.name, style=discord.ButtonStyle.secondary, row=2)

        async def callback(interaction: discord.Interaction):
            self.selected_facility = facility
            await self._update_button_styles()
            embed = self.embeds.get(facility)
            if embed:
                await interaction.response.edit_message(embed=embed, view=self)

        button.callback = callback
        return button

    async def _page_left(self, interaction: discord.Interaction):
        self.left_index -= 1
        await self._render_carousel_page()
        await self._update_button_styles()
        await interaction.response.edit_message(embed=self.initial_embed(), view=self)

    async def _page_right(self, interaction: discord.Interaction):
        self.left_index += 1
        await self._render_carousel_page()
        await self._update_button_styles()
        await interaction.response.edit_message(embed=self.initial_embed(), view=self)

    async def _update_button_styles(self):
        for facility, button in self.facility_buttons.items():
            button.style = (
                discord.ButtonStyle.primary
                if facility == self.selected_facility
                else discord.ButtonStyle.secondary
            )

    def initial_embed(self) -> discord.Embed:
        return self.embeds.get(self.selected_facility, discord.Embed(title="Facilities"))

    async def add_callback(self, interaction: discord.Interaction):
        num_available = await self.bastion.get_num_facilities_needing_construction()
        if num_available <= 0:
            await interaction.response.send_message("Your bastion is not ready for another facility", ephemeral=True)
            return

        if self.selected_facility in self.bastion.facilities["owned"]:
            await interaction.response.send_message(f"Your bastion already has a {self.selected_facility.name}",
                                                    ephemeral=True)
            return

        self.bastion.facilities["owned"].add(self.selected_facility)

        self.left_index = 0
        await self._render_carousel_page()
        await interaction.response.edit_message(embed=self.initial_embed(), view=self)
        # Was 1, is now 0
        if num_available == 1:
            new_view = await AboutBastionView.create(self.bastion)
            await interaction.followup.edit_message(
                message_id=interaction.message.id,
                embed=new_view.initial_embed(),
                view=new_view
            )

        view = await SpecialFacilityView.create(self.selected_facility, self.bastion.owner)
        await interaction.followup.send(embed=view.main_view, view=view)
