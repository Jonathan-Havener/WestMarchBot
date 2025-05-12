import discord
from discord import ui
from discord.ui import View, Select, select

from routes.player_factory import PlayerFactory


class ReceiptDropdownView(View):
    def __init__(self, threads, item_name, price, purchaser, shop):
        super().__init__(timeout=60)
        self.item_name = item_name
        self.price = price
        self.purchaser = purchaser
        self.shop = shop

        options = [
            discord.SelectOption(label=thread.name, value=str(thread.id))
            for thread in threads if thread is not None
        ]

        self.add_item(ReceiptSelect(options, item_name, price, purchaser, self.shop))


class ReceiptSelect(Select):
    def __init__(self, options, item_name, price, purchaser, shop):
        super().__init__(placeholder="Choose a character thread to send the receipt to...", options=options)
        self.item_name = item_name
        self.price = price
        self.purchaser = purchaser
        self.shop = shop

    async def callback(self, interaction: discord.Interaction):
        thread_id = int(self.values[0])
        thread = interaction.client.get_channel(thread_id)
        if not thread:
            thread = await interaction.client.fetch_channel(thread_id)

        embed = discord.Embed(
            title="🧾 Item Purchase Receipt",
            color=discord.Color.gold(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="Customer", value=thread.name, inline=True)
        embed.add_field(name="Shop", value=self.shop.name, inline=True)
        embed.add_field(name="\u200B", value="\u200B", inline=False)  # Spacer
        embed.add_field(name="Item", value=f"**{self.item_name}**", inline=True)
        embed.add_field(name="Price", value=f"{self.price} gold", inline=True)

        embed.set_footer(text="Thank you for your purchase!")

        await thread.send(embed=embed)

        await interaction.response.edit_message(
            content="🧾 Receipt sent!", view=None
        )


class ShopView(ui.View):
    def __init__(self, bot, shop_logic, message, embed, timeout=60*60*24):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.shop = shop_logic
        self.message = message  # The original embed message
        self.embed = embed
        self.update_buttons()

    def update_buttons(self):
        self.clear_items()
        for idx, listing in enumerate(self.shop.inventory):
            label = f"Purchase {listing['item']['name'].title()}"

            async def button_callback(interaction):
                await self.interaction_handler(interaction)

            button = ui.Button(label=label, style=discord.ButtonStyle.primary, custom_id=str(idx))
            button.callback = button_callback
            self.add_item(button)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return True  # Add permission checks if needed

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        if hasattr(self, 'message'):
            await self.message.edit(view=self)

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: ui.Item):
        await interaction.response.send_message("An error occurred.", ephemeral=True)

    async def interaction_handler(self, interaction: discord.Interaction):
        try:
            index = int(interaction.data['custom_id'])
            listing = self.shop.inventory[index]
            item_name = listing['item']["name"]
            price = listing['price']

            # Update shop inventory
            self.shop.sell(item_name)
            self.embed.items = [item for item in self.embed.items if item['item']["name"] != item_name]

            # Refresh buttons after inventory changes
            self.update_buttons()

            # Update the shop embed message
            await self.message.edit(embed=self.embed, view=self)

            # Get character threads
            purchaser_id = interaction.user.id
            factory = PlayerFactory(self.bot)
            player_cog, _ = await factory.get_cog(purchaser_id)
            character_cogs = await player_cog.character_cogs()
            character_threads = [await cog.get_character_thread() for cog in character_cogs]

            # Send dropdown to user
            await interaction.response.send_message(
                "Which character thread should receive the purchase receipt?",
                view=ReceiptDropdownView(character_threads, item_name, price, interaction.user, self.shop),
                ephemeral=True
            )

        except (ValueError, IndexError):
            await interaction.response.send_message("Invalid item selected.", ephemeral=True)
