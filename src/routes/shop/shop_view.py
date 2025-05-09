import discord
from discord import ui


class ShopView(ui.View):
    def __init__(self, shop_logic, message, embed, timeout=60*60*24):
        super().__init__(timeout=timeout)
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

            # Update the shop embed message (remove item and refresh buttons)
            await self.message.edit(embed=self.embed, view=self)

            await interaction.response.send_message(
                f"You purchased the **{item_name}** for {price}g!",
                ephemeral=True
            )

        except (ValueError, IndexError):
            await interaction.response.send_message("Invalid item selected.", ephemeral=True)

