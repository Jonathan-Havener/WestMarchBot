from views.bastion.special_facility_base_embed import SpecialFacilityBaseEmbed


class SpecialFacilityInfoEmbed(SpecialFacilityBaseEmbed):
    @classmethod
    async def create(cls, facility, owner):
        self = await SpecialFacilityBaseEmbed.create(facility, owner)

        self.add_field(name="Size", value=facility.space, inline=True)
        self.add_field(name="Hirelings", value=facility.hirelings, inline=True)
        self.add_field(name="Level Requirement", value=facility.level_requirement)

        if facility.prerequisite:
            self.set_footer(text=f"Requires: {facility.prerequisite}")

        return self
