import os
from pathlib import Path

import yaml
import discord
from discord import ui
import asyncio


FILTER_TYPES = ["Armor", "Potion", "Ring", "Rod", "Scroll", "Staff", "Wand", "Weapon", "Wondrous item"]
RARITIES = ["Common", "Uncommon", "Rare", "Very Rare", "Legendary"]


class FilterSession:
    def __init__(self):
        self.shop_name = None
        self.filter_type = set()
        self.rarity = set()
        self.item_text = ""

    def to_dict(self):
        return {
            "filter": {
                "keyParams": {
                    "filterType": list(self.filter_type),
                    "rarity": list(self.rarity)
                },
                "name": self.shop_name,
                "itemText": self.item_text
            }
        }

    def to_pretty_yaml(self):
        return yaml.dump(self.to_dict(), sort_keys=False)


class CreateShopView(ui.View):
    def __init__(self, session: FilterSession, magic_manager):
        super().__init__(timeout=None)
        self.session = session
        self.page = "nameEntry"  # or "rarity"
        self.magic_man = magic_manager

    def get_embed(self):
        if self.page == "filterType":
            selected = ', '.join(self.session.filter_type) or "None"
            title = "Select Item Types"
            description = f"Click to toggle types. Currently selected: {selected}"
        elif self.page == "rarity":
            selected = ', '.join(self.session.rarity) or "None"
            title = "Select Rarities"
            description = f"Click to toggle rarities. Currently selected: {selected}"
        elif self.page == "nameEntry":
            title = "Enter Shop Name"
            description = f"Current name: {self.session.shop_name or 'Not set'}"
        elif self.page == "nameContains":
            title = "Item Name Filter"
            description = f"Current name: {self.session.shop_name or 'Not set'}"
        else:
            title = "Unknown Page"
            description = "Something went wrong."

        embed = discord.Embed(title=title, description=description, color=0x00bfff)
        embed.set_footer(text="Use the navigation buttons to change pages.")
        return embed

    async def update_message(self, interaction: discord.Interaction):
        self.refresh_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @ui.button(label="Set Shop Name", style=discord.ButtonStyle.primary, row=1)
    async def set_shop_name(self, interaction: discord.Interaction, button: ui.Button):
        if self.page != "nameEntry":
            return
        await interaction.response.send_modal(ShopNameModal(self))

    @ui.button(label="Shop Name", style=discord.ButtonStyle.secondary, row=2)
    async def to_name_entry(self, interaction: discord.Interaction, button: ui.Button):
        self.page = "nameEntry"
        await self.update_message(interaction)

    @ui.button(label="Magic Item Type", style=discord.ButtonStyle.secondary, row=2)
    async def to_filter_type(self, interaction: discord.Interaction, button: ui.Button):
        self.page = "filterType"
        await self.update_message(interaction)

    @ui.button(label="Rarity", style=discord.ButtonStyle.secondary, row=2)
    async def to_rarity(self, interaction: discord.Interaction, button: ui.Button):
        self.page = "rarity"
        await self.update_message(interaction)

    @ui.button(label="Set Item Name Filter", style=discord.ButtonStyle.primary, row=1)
    async def set_name_filter(self, interaction: discord.Interaction, button: ui.Button):
        if self.page != "nameContains":
            return
        await interaction.response.send_modal(MagicItemNameFilter(self))

    @ui.button(label="Name Contains...", style=discord.ButtonStyle.secondary, row=2)
    async def to_name_contains(self, interaction: discord.Interaction, button: ui.Button):
        self.page = "nameContains"
        await self.update_message(interaction)

    @ui.button(label="Done", style=discord.ButtonStyle.success, row=2)
    async def done(self, interaction: discord.Interaction, button: ui.Button):
        pretty_yaml = self.session.to_pretty_yaml()

        message = f"Here are the items that might appear in your shop!\n"
        item_list = [item["name"] for item in self.magic_man.get_filtered_items(self.session.to_dict()["filter"])]
        message += '\n'.join(item_list)
        await interaction.response.send_message(message, ephemeral=True)

        message = f"Here's your shop filter YAML:\n{self.session.shop_name}\n```\n{pretty_yaml}```"
        bot = interaction.client
        admin = bot.get_user(int(os.environ.get("ADMIN_ID")))
        await admin.send(message)

        output_path = Path(
            __file__).parent.parent.parent.parent / "data" / "shop_definitions" / f"{self.session.shop_name}.yml"
        with open(output_path, "w") as file:
            yaml.dump(self.session.to_dict(), file, sort_keys=False)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return True

    def get_buttons(self):
        return FILTER_TYPES if self.page == "filterType" else RARITIES

    async def on_timeout(self):
        self.clear_items()

    def refresh_buttons(self):
        self.clear_items()

        if self.page == "filterType":
            for item in FILTER_TYPES:
                self.add_item(OptionButton(item, self))
        elif self.page == "rarity":
            for item in RARITIES:
                self.add_item(OptionButton(item, self))
        elif self.page == "nameEntry":
            self.add_item(self.set_shop_name)
        elif self.page == "nameContains":
            self.add_item(self.set_name_filter)

        # Navigation buttons (always shown)
        self.add_item(self.to_name_entry)
        self.add_item(self.to_filter_type)
        self.add_item(self.to_rarity)
        self.add_item(self.to_name_contains)
        self.add_item(self.done)

    async def on_ready(self, message):
        self.refresh_buttons()
        await message.edit(embed=self.get_embed(), view=self)


class OptionButton(ui.Button):
    def __init__(self, label: str, parent_view: CreateShopView):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.parent_view = parent_view

    async def callback(self, interaction: discord.Interaction):
        value_set = self.parent_view.session.filter_type if self.parent_view.page == "filterType" else self.parent_view.session.rarity

        if self.label in value_set:
            value_set.remove(self.label)
        else:
            value_set.add(self.label)

        await self.parent_view.update_message(interaction)


class ShopNameModal(ui.Modal, title="Set Shop Name"):
    shop_name = ui.TextInput(label="Enter shop name", placeholder="e.g. Goblin's Gears", max_length=100)

    def __init__(self, view: CreateShopView):
        super().__init__()
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):
        self.view.session.shop_name = self.shop_name.value
        await self.view.update_message(interaction)


class MagicItemNameFilter(ui.Modal, title="Filter Item Names"):
    item_text = ui.TextInput(label="Enter something your shop specializes in",
                             placeholder="e.g. \"Swords\" will make sure all items have sword in the name.",
                             max_length=100)

    def __init__(self, view: CreateShopView):
        super().__init__()
        self.view = view

    async def on_submit(self, interaction: discord.Interaction):
        self.view.session.item_text = self.item_text.value
        await self.view.update_message(interaction)

