from logic.bastion.special_facility import SpecialFacility


class Storehouse(SpecialFacility):
    level_requirement = 5
    name = "Storehouse"
    prerequisite = ""
    order = "Trade"
    description = ("A Storehouse is a cool, dark space meant to contain trade goods objects from the Trade Goods table "
                   "in chapter 7 and from chapter 6 of the Player's Handbook.")
    space = "Roomy"
    hirelings = 1
