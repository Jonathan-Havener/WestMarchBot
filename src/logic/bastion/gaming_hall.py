from logic.bastion.special_facility import SpecialFacility


class GamingHall(SpecialFacility):
    level_requirement = 9
    name = "Gaming Hall"
    prerequisite = ""
    order = "Trade"
    description = "A Gaming Hall offers recreational activities like chess and games of darts, cards, or dice."
    space = "Vast"
    hirelings = 4
