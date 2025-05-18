from logic.bastion.choice import Choice
from views.bastion.special_facility_base_view import SpecialFacilityBaseEmbed


class ChoiceEmbed(SpecialFacilityBaseEmbed):
    @classmethod
    async def create(cls, facility, owner, choice: "Choice"):
        self = await SpecialFacilityBaseEmbed.create(facility, owner)
        self.choice = choice
        self.description = choice.description

        self.add_field(name="Order Type", value=choice.order_type, inline=True)
        if choice.craft_time:
            self.add_field(name="Craft Time", value=choice.craft_time, inline=True)
        if choice.duration:
            self.add_field(name="Duration", value=choice.duration, inline=True)
        if choice.cost:
            self.add_field(name="Cost", value=f"{choice.cost} GP", inline=True)
        self.add_field(name="Level Requirement", value=choice.level_requirement)

        return self
