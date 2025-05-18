from logic.bastion.choice import Choice
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

    def __init__(self, owner):
        super().__init__(owner)

        desc = ""
        choice = Choice(name="", description=desc)
        self.choices.append(choice)

        desc = ""
        choice = Choice(name="", description=desc, order_type="")
        self.choices.append(choice)
