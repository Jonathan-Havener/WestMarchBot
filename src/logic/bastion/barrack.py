from logic.bastion.special_facility import SpecialFacility


class Barrack(SpecialFacility):
    level_requirement = 5
    name = "Barrack"
    prerequisite = ""
    order = "Recruit"
    description = ("A Bastion can have more than one Barrack, each of which is furnished to serve as sleeping quarters "
                   "for up to twelve Bastion Defenders.")
    space = "Roomy"
    hirelings = 1
