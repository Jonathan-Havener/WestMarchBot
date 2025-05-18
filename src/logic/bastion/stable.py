from logic.bastion.choice import Choice
from logic.bastion.special_facility import SpecialFacility


class Stable(SpecialFacility):
    level_requirement = 9
    name = "Stable"
    prerequisite = ""
    order = "Trade"
    description = ("A Bastion can have more than one Stable. Each Stable you add to your Bastion comes with one Riding"
                   " Horse or Camel and two Ponies or Mules; see the Player’s Handbook or the Monster Manual for these"
                   " creatures’ stat blocks. The facility is big enough to house three Large animals. Two Medium "
                   "creatures occupy the same amount of space as one Large creature there. The facility’s hireling "
                   "looks after these creatures.\n\nAfter a Beast that can serve as a mount spends at least 14 days in"
                   " this facility, all Wisdom (Animal Handling) checks made with respect to it have Advantage.")
    space = "Roomy"
    hirelings = 1

    def __init__(self, owner):
        super().__init__(owner)

        desc = ("You can enlarge your Stable to a Vast facility by spending 2,000 GP. If you do so, the Stable is "
                "large enough to house six Large animals.")
        choice = Choice(name="Enlarging the Facility", description=desc, cost=2000)
        self.choices.append(choice)

        desc = ("When you issue the Trade order to this facility, you commission the facility’s hireling to buy or sell"
                " one or more mounts at normal cost, keeping the ones you buy in your Stable. The work takes 7 days, "
                "and the DM decides what types of animals are available for purchase—horses, ponies, and mules being"
                " the most common. The Mounts and Other Animals table in the Player’s Handbook gives standard prices "
                "for various mounts. You bear the total cost of any purchases.\n\nWhen you sell a mount from your "
                "Stable, the buyer pays you 20 percent more than the standard price; this profit increases to 50 "
                "percent when you reach level 13 and 100 percent when you reach level 17.")
        choice = Choice(name="Trade: Animals", description=desc, order_type="Trade")
        self.choices.append(choice)
