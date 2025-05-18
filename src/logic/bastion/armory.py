from logic.bastion.special_facility import SpecialFacility


class Armory(SpecialFacility):
    level_requirement = 5
    name = "Armory"
    prerequisite = ""
    order = "Trade"
    description = ("An Armory contains mannequins for displaying armor, hooks for holding Shields, racks for storing "
                   "weapons, and chests for holding ammunition.")
    space = "Roomy"
    hirelings = 1
