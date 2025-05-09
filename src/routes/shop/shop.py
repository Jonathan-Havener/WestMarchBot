from discord.ext import commands
import discord
from pathlib import Path

from logic.shop_bot import Shop as ShopLogic
from logic.shop_bot import MagicManager

from .shop_view import ShopView
from .magic_item_embed import MagicItemEmbed


class Shop(commands.Cog):
    def __init__(self, bot):
        print("Shop initialized")
        self.bot = bot

        magic_manager = MagicManager(source=Path(__file__).parent.parent.parent.parent / "data" / "dmg-magic-item-definitions.json")
        self._shop = ShopLogic(magic_manager_obj=magic_manager)
        self._shop.fill_inventory()

    @commands.command()
    async def shop(self, ctx):
        embed = MagicItemEmbed(
            title="Verdelume Guild Shop",
            description="Browse our selection of magical items below!",
            color=discord.Color.gold(),
            listings=self._shop.inventory
        )
        message = await ctx.send(embed=embed)

        view = ShopView(self._shop, message=message, embed=embed)  # Pass the embed to the view
        await message.edit(view=view)

    @commands.command()
    async def stock_shops(self, ctx):
        self._shop.fill_inventory()
        await ctx.send('Inventory Filled!')
