from discord.ext import commands
import discord
from pathlib import Path
import asyncio

from ..logic.shop_bot import ShopBuilder
from ..logic.shop_bot import MagicManager
from .routine import Routine


class MagicItemEmbed(discord.Embed):
    def __init__(self, title, description, color, listings):
        super().__init__(title=title, description=description, color=color)
        # Set the footer, author, and thumbnail (optional)
        self.set_footer(text="Good luck, adventurer!")
        self.set_author(name="Verdelume Guild")
        self.set_thumbnail(url="https://example.com/dragon_thumbnail.png")  # Replace with an actual image URL

        self._items = {}
        self.items = listings

    @property
    def items(self) -> dict:
        return self._items

    def get_item_properties(self, magic_item) -> dict:
        prop = {
            "Rarity": magic_item.rarity,
            "Item Type": magic_item.item_type,
            "Attunement": magic_item.attunement,
            "impact": magic_item.impact
        }
        return prop

    @items.setter
    def items(self, magic_item_listings):
        self._items = {}
        self.clear_fields()
        available_reacts = [
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
        ]
        for listing in magic_item_listings:
            this_emoji = available_reacts.pop(0)
            self._items.update({this_emoji: listing})
            details = [
                f"**{key.title()}:** {self.get_item_properties(listing['item'])[key]}"
                for key in self.get_item_properties(listing["item"])
            ]
            details += [f"**Price:** {listing['price']}"]
            details = "\n".join(details)
            self.add_field(
                name=f"{this_emoji} : **{listing['item'].name.title()}**",
                value=details,
                inline=False  # Ensures each item is listed on a new line
            )


class Shop(Routine):
    def __init__(self, bot):
        print("Shop initialized")
        self.bot = bot

        shop_definitions = Path(r"/data/shop_definitions")
        self._shops = ShopBuilder().build_shops(shop_definitions)

        bot_updates_channel_id = 1293370203060830279
        self.ctx = self.bot.get_channel(bot_updates_channel_id)

        self._shop_uis = []

        super().__init__()

    # def __del__(self):
    #     loop = self.clean_up()
    #     while True:
    #         pending = asyncio.all_tasks(loop=loop)
    #         if not pending:
    #             break
    #     print("Done")
    #
    # def clean_up(self):
    #     loop = asyncio.get_event_loop()
    #
    #     for shop in self._shop_uis:
    #         asyncio.run_coroutine_threadsafe(shop.delete(), loop)
    #     return loop

    async def process(self):
        await asyncio.gather(*[self.setup_shop(shop) for shop in self._shops])

    async def setup_shop(self, shop):
        # Create an embed (card)
        embed = MagicItemEmbed(
            title=shop.name,
            description="Embark on a journey across Verdelume!",
            color=discord.Color.blue(),  # Embed color
            listings=shop.inventory
        )

        thread = next((thread for thread in self.ctx.threads if thread.name == shop.name), None)
        if not thread:
            thread, _ = await self.ctx.create_thread(content=shop.description, name=shop.name)
        message = await thread.send(embed=embed)
        self._shop_uis.append(message)

        for emoji in embed.items:
            await message.add_reaction(emoji)

        while len(embed.items) > 0:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add",
                    check=lambda user_reaction, responding_user:
                    responding_user != self.bot.user and user_reaction.message.id == message.id)

                # Find the item corresponding to the reaction
                selected_listing = embed.items.get(reaction.emoji, None)

                if selected_listing:
                    # Remove the selected item from the list
                    shop.sell(selected_listing["item"].name)

                    # Edit the embed to update the list of items
                    embed.items = shop.inventory

                    await message.edit(embed=embed)

                    await thread.send(
                        f"{user.mention} purchased **{selected_listing['item'].name}** for {selected_listing['price']}g!")

                    await message.clear_reactions()
                    for emoji in embed.items:
                        await message.add_reaction(emoji)

            except asyncio.TimeoutError:
                await thread.send("Shop timed out! Please try again later.")
                break
