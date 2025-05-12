import logging
import os

from discord.ext import commands
import discord
from pathlib import Path

from logic.shop_bot import ShopBuilder
from logic.shop_bot import MagicManager

from .shop_view import ShopView
from .magic_item_embed import MagicItemEmbed
from .create_shop_view import CreateShopView, FilterSession
from .shop_browser_view import ShopBrowserView

import yaml


class Shop(commands.Cog):
    def __init__(self, bot):
        self._shops = None
        logging.info("Shop initialized")
        self.bot = bot

        self.shop_forum = self.bot.get_channel(int(os.environ.get("SHOPS_ID")))

        self.magic_manager = MagicManager(source=Path(__file__).parent.parent.parent.parent / "data" / "dmg-magic-item-definitions.json")
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
                    filters.append(data.get("filter", {}))
                except Exception as e:
                    await ctx.send(f"Failed to read {file.name}: {e}")

        view = ShopBrowserView(filters, self.magic_manager)
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

            view = ShopView(self.bot, shop, message=message, embed=embed)
            await message.edit(view=view)

    @commands.command(
        help="Create a shop with the given name, or be prompted to enter one if not provided."
    )
    async def create_shop(self, ctx):
        session = FilterSession()

        view = CreateShopView(session, self.magic_manager)
        message = await ctx.send(embed=view.get_embed(), view=view)
        await view.on_ready(message)

    # @commands.command()
    # async def stock_shops(self, ctx):
    #     self._shop.fill_inventory()
    #     await ctx.send('Inventory Filled!')
