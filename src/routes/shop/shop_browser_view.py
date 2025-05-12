import discord
from discord import ui, Embed


class ShopBrowserView(ui.View):
    def __init__(self, filters: list[dict], magic_manager, timeout=None):
        super().__init__(timeout=timeout)
        self.filters = filters
        self.index = 0
        self.message = None
        self.magic_man = magic_manager

    def format_embed(self):
        data = self.filters[self.index]

        embed = discord.Embed(
            title="Create Magic Item Shops",
            color=0x00bfff
        )
        embed.set_footer(text="Use the navigation buttons to change pages.")

        # Fields
        name_value = data["name"] or "*Not set*"
        embed.add_field(name="🛍️ Shop Name", value=name_value, inline=False)

        text_value = data.get("itemText", None) or "*No filter*"
        embed.add_field(name="🔍 Item Name Contains", value=text_value, inline=False)

        type_value = ', '.join(sorted(data.get("keyParams", {}).get("filterType", {}))) or "*None selected*"
        embed.add_field(name="📦 Item Types", value=type_value, inline=False)

        rarity_value = ', '.join(sorted(data.get("keyParams", {}).get("rarity", {}))) or "*None selected*"
        embed.add_field(name="✨ Rarities", value=rarity_value, inline=False)

        # Explicit filter check before showing item list
        filter_data = data
        key_params = filter_data.get("keyParams", {})
        filter_type = key_params.get("filterType", [])
        rarity = key_params.get("rarity", [])
        item_text = filter_data.get("itemText", "")

        has_filters = bool(item_text.strip()) or bool(filter_type) or bool(rarity)

        if not has_filters:
            embed.add_field(
                name="📋 Matching Items",
                value="*Apply filters to see matching items.*",
                inline=False,
            )

        else:
            filtered_items = self.magic_man.get_filtered_items(filter_data)
            item_names = [item["name"] for item in filtered_items]

            if not item_names:
                embed.add_field(
                    name="📋 Matching Items",
                    value="*No items match your filters.*",
                    inline=False,
                )
            else:
                preview_lines = []
                char_count = 0
                for name in item_names:
                    line = f"• {name}"
                    if char_count + len(line) + 1 > 1000:
                        break
                    preview_lines.append(line)
                    char_count += len(line) + 1

                if not preview_lines:
                    embed.add_field(
                        name="📋 Matching Items",
                        value=f"Too many items to show in preview. ({len(item_names)} items found)",
                        inline=False,
                    )
                else:
                    remaining = len(item_names) - len(preview_lines)
                    value = "\n".join(preview_lines)
                    if remaining > 0:
                        value += f"\n… and {remaining} more"
                    embed.add_field(
                        name="📋 Matching Items",
                        value=value,
                        inline=False,
                    )

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

