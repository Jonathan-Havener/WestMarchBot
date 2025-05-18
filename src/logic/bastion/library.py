from logic.bastion.choice import Choice
from logic.bastion.special_facility import SpecialFacility


class Library(SpecialFacility):
    level_requirement = 5
    name = "Library"
    prerequisite = ""
    order = "Research"
    description = "This Library contains a collection of books plus one or more desks and reading chairs."
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
