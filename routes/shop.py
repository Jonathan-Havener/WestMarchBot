from discord.ext import commands
import discord
from pathlib import Path
import sys
import asyncio

this_file = Path(__file__).parent
shop_bot_root_path = this_file.parent / "logic"
sys.path.append(str(shop_bot_root_path))
from shop_bot import Shop as ShopLogic
from shop_bot import MagicManager


class MagicItemEmbed(discord.Embed):
    def __init__(self, title, description, color, magicItems):
        super().__init__(title=title, description=description, color=color)
        # Set the footer, author, and thumbnail (optional)
        self.set_footer(text="Good luck, adventurer!")
        self.set_author(name="Verdelume Guild")
        self.set_thumbnail(url="https://example.com/dragon_thumbnail.png")  # Replace with an actual image URL

        self._items = {}
        self.items = magicItems

    @property
    def items(self) -> dict:
        return self._items

    @items.setter
    def items(self, magic_item_list):
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
        for item in magic_item_list:
            this_emoji = available_reacts.pop(0)
            self._items.update({this_emoji: item })
            details = [f"**{key.title()}:** {item.__dict__[key]}" for key in item.__dict__ if not key.startswith("_")]
            details = "\n".join(details)
            self.add_field(
                name=f"{this_emoji} : **{item.name.title()}**",
                value=details,
                inline=False  # Ensures each item is listed on a new line
            )


class Shop(commands.Cog):
    def __init__(self, bot):
        print("Shop cog initialized")
        self.bot = bot
        magic_manager = MagicManager(source=this_file.parent / "data" / "Magic Item Distribution - Items.csv")
        self._shop = ShopLogic(magic_manager_obj=magic_manager)
        self._shop.fill_inventory()

    @commands.command(guild_messages=True)
    async def shop(self, ctx):
        # Create an embed (card)
        embed = MagicItemEmbed(
            title="Adventure Quest",
            description="Embark on a journey across Verdelume!",
            color=discord.Color.blue(), # Embed color
            magicItems=self._shop.inventory
        )

        message = await ctx.send(embed=embed)

        for emoji in embed.items:
            await message.add_reaction(emoji)

        # Wait for a reaction from the user
        def check(user_reaction, responding_user):
            return responding_user != self.bot.user and user_reaction.message.id == message.id

        while len(embed.items) > 0:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=check)

                # Find the item corresponding to the reaction
                selected_item = embed.items.get(reaction.emoji, None)

                if selected_item:
                    # Remove the selected item from the list
                    self._shop.sell(selected_item.name)

                    # Edit the embed to update the list of items
                    embed = MagicItemEmbed(
                        title="Adventure Quest",
                        description="Embark on a journey across Verdelume!",
                        color=discord.Color.blue(), # Embed color
                        magicItems=self._shop.inventory
                    )
                    await message.edit(embed=embed)
                    await message.clear_reactions()
                    for emoji in embed.items:
                        await message.add_reaction(emoji)

                    # Optionally, send a message to the user confirming the purchase
                    await ctx.send(
                        f"{user.mention} purchased **{selected_item.name}** for {0}g!")

            except asyncio.TimeoutError:
                await ctx.send("Shop timed out! Please try again later.")
                break


    @commands.command(guild_messages=True)
    async def stock_shops(self, ctx):
        self._shop.fill_inventory()
        await ctx.send('Inventory Filled!')