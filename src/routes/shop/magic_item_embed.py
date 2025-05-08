import discord


class MagicItemEmbed(discord.Embed):
    def __init__(self, title, description, color, listings):
        super().__init__(title=title, description=description, color=color)
        # Set the footer, author, and thumbnail (optional)
        self.set_footer(text="Good luck, adventurer!")
        self.set_author(name="Verdelume Guild")
        self.set_thumbnail(url="https://example.com/dragon_thumbnail.png")  # Replace with an actual image URL

        self._items = []
        self.items = listings

    @property
    def items(self) -> list:
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
        self._items = []
        self.clear_fields()

        for listing in magic_item_listings:
            self._items.append(listing)
            details = [
                f"**{key.title()}:** {self.get_item_properties(listing['item'])[key]}"
                for key in self.get_item_properties(listing["item"])
            ]
            details += [f"**Price:** {listing['price']}"]
            details = "\n".join(details)
            self.add_field(
                name=f"= **{listing['item'].name.title()}** =",
                value=details,
                inline=False  # Ensures each item is listed on a new line
            )
