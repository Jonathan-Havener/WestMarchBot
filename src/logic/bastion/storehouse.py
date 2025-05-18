from logic.bastion.choice import Choice
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

    def __init__(self, owner):
        super().__init__(owner)

        desc = ("When you issue the Trade order to this facility, its hireling spends the next 7 days procuring "
                "nonmagical items that have a total value of 500 GP or less and stores them in the Storehouse, or the"
                " hireling uses those 7 days to sell goods in the Storehouse. You bear the total cost of any purchases,"
                " and the maximum value of the items purchased increases to 2,000 GP when you reach level 9 and 5,000 "
                "GP when you reach level 13.\n\nWhen you sell goods from your Storehouse, the buyer pays you 10 percent"
                " more than the standard price; this profit increases to 20 percent when you reach level 9, 50 percent"
                " when you reach level 13, and 100 percent when you reach level 17.")
        choice = Choice(name="Trade: Goods", description=desc, order_type="Trade")
        self.choices.append(choice)
