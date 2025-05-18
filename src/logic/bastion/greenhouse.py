from logic.bastion.special_facility import SpecialFacility


class Greenhouse(SpecialFacility):
    level_requirement = 9
    name = "Greenhouse"
    prerequisite = ""
    order = "Harvest"
    description = "A Greenhouse is an enclosure where rare plants and fungi are nurtured in a controlled climate."
    space = "Roomy"
    hirelings = 1
