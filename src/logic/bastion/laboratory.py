from logic.bastion.special_facility import SpecialFacility


class Laboratory(SpecialFacility):
    level_requirement = 9
    name = "Laboratory"
    prerequisite = ""
    order = "Craft"
    description = ("A Laboratory contains storage space for alchemical supplies and workspaces for crafting various "
                   "concoctions.")
    space = "Roomy"
    hirelings = 1
