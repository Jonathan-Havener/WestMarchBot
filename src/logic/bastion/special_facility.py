class SpecialFacility:
    level_requirement = 5
    name = "Special Facility"
    prerequisite = ""
    order = ""
    description = "A template for special facilities."
    space = "Roomy"
    hirelings = 1

    def __init__(self, owner: "character_cog"):
        self.owner = owner
        self.choices = []
