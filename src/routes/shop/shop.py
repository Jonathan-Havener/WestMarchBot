import logging
import os

from discord.ext import commands
import discord
from pathlib import Path

from logic.shop_bot import Shop as ShopLogic
from logic.shop_bot import ShopBuilder
from logic.shop_bot import MagicManager

from .shop_view import ShopView
from .magic_item_embed import MagicItemEmbed
import asyncio


FILTER_TYPES = ["Armor", "Potion", "Ring", "Rod", "Scroll", "Staff", "Wand", "Weapon", "Wondrous item"]
RARITIES = ["Common", "Uncommon", "Rare", "Very Rare", "Legendary"]


class FilterSession:
    def __init__(self):
        self.shop_name = None
        self.filter_type = set()
        self.rarity = set()

    def to_dict(self):
        return {
            "filter": {
                "filterType": list(self.filter_type),
                "rarity": list(self.rarity)
            }
        }

    def to_pretty_yaml(self):
        return yaml.dump(self.to_dict(), sort_keys=False)


from discord import ui
import yaml


class ShopFilterView(ui.View):
    def __init__(self, session: FilterSession):
        super().__init__(timeout=None)
        self.session = session
        self.page = "filterType"  # or "rarity"

    def get_embed(self):
        if self.page == "filterType":
            selected = ', '.join(self.session.filter_type) or "None"
            title = "Select Item Types"
            description = f"Click to toggle types. Currently selected: {selected}"
            options = FILTER_TYPES
        else:
            selected = ', '.join(self.session.rarity) or "None"
            title = "Select Rarities"
            description = f"Click to toggle rarities. Currently selected: {selected}"
            options = RARITIES

        embed = discord.Embed(title=title, description=description, color=0x00bfff)
        embed.set_footer(text="Use the navigation buttons to change pages.")
        return embed

    async def update_message(self, interaction: discord.Interaction):
        self.refresh_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @ui.button(label="<< Filter Type", style=discord.ButtonStyle.secondary, row=2)
    async def to_filter_type(self, interaction: discord.Interaction, button: ui.Button):
        self.page = "filterType"
        await self.update_message(interaction)

    @ui.button(label="Rarity >>", style=discord.ButtonStyle.secondary, row=2)
    async def to_rarity(self, interaction: discord.Interaction, button: ui.Button):
        self.page = "rarity"
        await self.update_message(interaction)

    @ui.button(label="Done", style=discord.ButtonStyle.success, row=2)
    async def done(self, interaction: discord.Interaction, button: ui.Button):
        pretty_yaml = self.session.to_pretty_yaml()

        await interaction.response.send_message("Here's your shop filter YAML:", ephemeral=True)
        await interaction.followup.send(f"```\n{pretty_yaml}```", ephemeral=True)

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
        # Clear all buttons
        self.clear_items()

        # Add new option buttons
        for item in self.get_buttons():
            self.add_item(OptionButton(item, self))

        # Re-add navigation buttons
        self.add_item(self.to_filter_type)
        self.add_item(self.to_rarity)
        self.add_item(self.done)

    async def on_ready(self, message):
        self.refresh_buttons()
        await message.edit(embed=self.get_embed(), view=self)


class OptionButton(ui.Button):
    def __init__(self, label: str, parent_view: ShopFilterView):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.parent_view = parent_view

    async def callback(self, interaction: discord.Interaction):
        value_set = self.parent_view.session.filter_type if self.parent_view.page == "filterType" else self.parent_view.session.rarity

        if self.label in value_set:
            value_set.remove(self.label)
        else:
            value_set.add(self.label)

        await self.parent_view.update_message(interaction)


from discord import ui, Embed

class ShopFilterBrowser(ui.View):
    def __init__(self, filters: list[tuple[str, dict]], *, timeout=180):
        super().__init__(timeout=timeout)
        self.filters = filters
        self.index = 0
        self.message = None

    def format_embed(self):
        name, data = self.filters[self.index]
        filter_type = ", ".join(data.get("filterType", [])) or "None"
        rarity = ", ".join(data.get("rarity", [])) or "None"

        embed = Embed(
            title=f"Shop Filter: {name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Filter Type", value=filter_type, inline=False)
        embed.add_field(name="Rarity", value=rarity, inline=False)
        embed.set_footer(text=f"{self.index + 1} / {len(self.filters)}")
        return embed

    async def on_ready(self, message):
        self.message = message
        await message.edit(embed=self.format_embed(), view=self)

    @ui.button(label="Previous", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: ui.Button):
        self.index = (self.index - 1) % len(self.filters)
        await interaction.response.edit_message(embed=self.format_embed(), view=self)

    @ui.button(label="Next", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: ui.Button):
        self.index = (self.index + 1) % len(self.filters)
        await interaction.response.edit_message(embed=self.format_embed(), view=self)

    @ui.button(label="Close", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.message.delete()
        self.stop()


class Shop(commands.Cog):
    def __init__(self, bot):
        self._shops = None
        logging.info("Shop initialized")
        self.bot = bot

        self.shop_forum = self.bot.get_channel(int(os.environ.get("SHOPS_ID")))

        magic_manager = MagicManager(source=Path(__file__).parent.parent.parent.parent / "data" / "dmg-magic-item-definitions.json")
        # self._shop = ShopLogic(magic_manager_obj=magic_manager)
        # self._shop.fill_inventory()

    @commands.command(
        help="Open a paginated browser of existing shop filters."
    )
    async def show_shops(self, ctx):
        shop_definitions_dir = Path(__file__).parent.parent.parent.parent / "data" / "shop_definitions"
        yaml_files = list(shop_definitions_dir.glob("*.yml"))

        if not yaml_files:
            await ctx.send("No shop filters found.")
            return

        filters = []
        for file in yaml_files:
            with open(file, "r") as f:
                try:
                    data = yaml.safe_load(f)
                    filters.append((file.stem, data.get("filter", {})))
                except Exception as e:
                    await ctx.send(f"Failed to read {file.name}: {e}")

        view = ShopFilterBrowser(filters)
        message = await ctx.send(embed=view.format_embed(), view=view)
        await view.on_ready(message)

    @commands.command(
        help="Post item listings for all shops, or only one if a name is provided."
    )
    async def shop(self, ctx, *, shop_name: str = None):
        this_file = Path(__file__).parent
        shop_definitions = this_file.parent.parent.parent / "data" / "shop_definitions"
        self._shops = ShopBuilder().build_shops(shop_definitions)

        # Filter to just the one shop if a name was provided
        shops_to_create = (
            [shop for shop in self._shops if shop.name.lower() == shop_name.lower()]
            if shop_name else self._shops
        )

        if not shops_to_create:
            await ctx.send(f"No shop found with the name '{shop_name}'.")
            return

        for shop in shops_to_create:
            embed = MagicItemEmbed(
                title=shop.name,
                description="Browse our selection of magical items below!",
                color=discord.Color.gold(),
                listings=shop.inventory
            )

            thread = next((t for t in self.shop_forum.threads if t.name == shop.name), None)
            if not thread:
                thread, _ = await self.shop_forum.create_thread(content=shop.description, name=shop.name)

            message = await thread.send(embed=embed)

            view = ShopView(shop, message=message, embed=embed)
            await message.edit(view=view)

    @commands.command(
        help="Create a shop with the given name, or be prompted to enter one if not provided."
    )
    async def create_shop(self, ctx, *, shop_name: str = None):
        if not shop_name:
            await ctx.send("What is the name of your shop?")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg = await self.bot.wait_for("message", check=check, timeout=60)
                shop_name = msg.content
            except asyncio.TimeoutError:
                await ctx.send("Timed out waiting for input.")
                return

        session = FilterSession()
        session.shop_name = shop_name

        view = ShopFilterView(session)
        message = await ctx.send(embed=view.get_embed(), view=view)
        await view.on_ready(message)

    # @commands.command()
    # async def stock_shops(self, ctx):
    #     self._shop.fill_inventory()
    #     await ctx.send('Inventory Filled!')
