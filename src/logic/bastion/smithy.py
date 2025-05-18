from logic.bastion.special_facility import SpecialFacility


class Smithy(SpecialFacility):
    level_requirement = 5
    name = "Smithy"
    prerequisite = ""
    order = "Craft"
    description = ("This Smithy contains a forge, an anvil, and other tools needed to craft weapons, armor, and other "
                   "equipment.")
    space = "Roomy"
    hirelings = 2
