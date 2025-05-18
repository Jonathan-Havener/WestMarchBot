from logic.bastion.special_facility import SpecialFacility


class Scriptorium(SpecialFacility):
    level_requirement = 9
    name = "Scriptorium"
    prerequisite = ""
    order = "Craft"
    description = "A Scriptorium contains desks and writing supplies."
    space = "Roomy"
    hirelings = 1
