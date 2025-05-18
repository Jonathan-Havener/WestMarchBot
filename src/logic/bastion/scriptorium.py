from logic.bastion.choice import Choice
from logic.bastion.special_facility import SpecialFacility


class Scriptorium(SpecialFacility):
    level_requirement = 9
    name = "Scriptorium"
    prerequisite = ""
    order = "Craft"
    description = "A Scriptorium contains desks and writing supplies."
    space = "Roomy"
    hirelings = 1

    def __init__(self, owner):
        super().__init__(owner)

        desc = ("You commission the facility’s hireling to make a copy of a nonmagical Book. Doing so requires a blank "
                "book. The work takes 7 days.")
        choice = Choice(name="Craft: Book Replica", description=desc, order_type="Craft")
        self.choices.append(choice)

        desc = ("You commission the facility’s hireling to scribe a Spell Scroll containing one Cleric or Wizard spell "
                "of level 3 or lower. The facility has the necessary Calligrapher’s Supplies, and the hireling meets "
                "all the prerequisites needed to scribe the scroll. The “Crafting Equipment” section in the Player’s "
                "Handbook specifies the time needed to scribe the scroll and the cost of the scroll, which you must "
                "pay.")
        choice = Choice(name="Craft: Spell Scroll", description=desc, order_type="Craft")
        self.choices.append(choice)

        desc = ("You commission the facility’s hireling to create up to fifty copies of a broadsheet, a pamphlet, or "
                "another loose-leaf paper product. The work takes 7 days and costs you 1 GP per copy. At no additional"
                " cost in time or money, the facility’s hireling can distribute the paperwork to one or more locations"
                " within 50 miles of your Bastion.")
        choice = Choice(name="Craft: Paperwork", description=desc, order_type="Craft")
        self.choices.append(choice)
