from logic.bastion.special_facility import SpecialFacility


class Workshop(SpecialFacility):
    level_requirement = 5
    name = "Workshop"
    prerequisite = ""
    order = "Craft"
    description = "This Workshop is a creative space where useful items can be crafted."
    space = "Roomy"
    hirelings = 3
