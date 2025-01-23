from discord.ext import commands
import discord
from pathlib import Path
import sys
import asyncio

this_file = Path(__file__).parent
from logic.shop_bot import Shop as ShopLogic
from logic.shop_bot import MagicManager


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


class Shop(commands.Cog):
    def __init__(self, bot):
        print("Shop initialized")
        self.bot = bot
        magic_manager = MagicManager(source=this_file.parent.parent / "data" /
                                            "Magic Item Distribution - Items.csv")
        self._shop = ShopLogic(magic_manager_obj=magic_manager)
        self._shop.fill_inventory()

    @commands.command(guild_messages=True)
    async def shop(self, ctx):
        # Create an embed (card)
        embed = MagicItemEmbed(
            title=self._shop.name,
            description="Embark on a journey across Verdelume!",
            color=discord.Color.blue(),# Embed color
            listings=self._shop.inventory
        )

        message = await ctx.send(embed=embed)

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
                    self._shop.sell(selected_listing["item"].name)

                    # Edit the embed to update the list of items
                    embed.items = self._shop.inventory

                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    for emoji in embed.items:
                        await message.add_reaction(emoji)

                    await ctx.send(
                        f"{user.mention} purchased **{selected_listing['item'].name}** for {selected_listing['price']}g!")

            except asyncio.TimeoutError:
                await ctx.send("Shop timed out! Please try again later.")
                break


    @commands.command(guild_messages=True)
    async def stock_shops(self, ctx):
        self._shop.fill_inventory()
        await ctx.send('Inventory Filled!')