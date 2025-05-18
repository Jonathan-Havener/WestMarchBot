from logic.bastion.choice import Choice
from logic.bastion.special_facility import SpecialFacility


class Sacristy(SpecialFacility):
    level_requirement = 9
    name = "Sacristy"
    prerequisite = "Ability to use a Holy Symbol or Druidic Focus as a Spellcasting Focus"
    order = "Craft"
    description = "A Sacristy serves as a preparation and storage room for the sacred items and religious vestments."
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
