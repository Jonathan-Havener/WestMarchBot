from logic.bastion.choice import Choice
from logic.bastion.special_facility import SpecialFacility


class GamingHall(SpecialFacility):
    level_requirement = 9
    name = "Gaming Hall"
    prerequisite = ""
    order = "Trade"
    description = "A Gaming Hall offers recreational activities like chess and games of darts, cards, or dice."
    space = "Vast"
    hirelings = 4

    def __init__(self, owner):
        super().__init__(owner)
        # TODO: Create Table

        desc = ("When you issue the Trade order to this facility, the facility’s hirelings turn the Gaming Hall into a "
                "gambling den for 7 days. At the end of the seventh day, roll 1d100 and consult the following table to"
                " determine your portion of the house’s winnings.")
        choice = Choice(name="Trade: Gambling Hall", description=desc, order_type="Trade")
        self.choices.append(choice)
