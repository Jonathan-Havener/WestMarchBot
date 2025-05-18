import discord

from views.bastion.navigable_bastion_view import NavigableBastionView


class AboutBastionView(NavigableBastionView):
    def __init__(self, bastion):
        super().__init__(bastion, section="about")

    @classmethod
    async def create(cls, bastion):
        return cls(bastion)

    def initial_embed(self) -> discord.Embed:
        return discord.Embed(
            title="About Bastions",
            description="Bastions are magical fortresses that evolve over time.\n\nUse the navigation buttons to switch sections."
        )
