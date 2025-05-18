from logic.bastion.choice import Choice
from logic.bastion.special_facility import SpecialFacility


class Barrack(SpecialFacility):
    level_requirement = 5
    name = "Barrack"
    prerequisite = ""
    order = "Recruit"
    description = ("A Bastion can have more than one Barrack, each of which is furnished to serve as sleeping quarters "
                   "for up to twelve Bastion Defenders.")
    space = "Roomy"
    hirelings = 1

    def __init__(self, owner):
        super().__init__(owner)

        desc = ("You can enlarge your Barrack to a Vast facility by spending 2,000 GP. A Vast Barrack can accommodate "
                "up to twenty-five Bastion Defenders.")
        choice = Choice(name="Enlarging the Facility", description=desc, cost=2000)
        self.choices.append(choice)

        desc = ("Each time you issue the Recruit order to this facility, up to four Bastion Defenders are recruited to"
                " your Bastion and assigned quarters in this Barrack. The recruitment costs no money. You can’t issue"
                " the Recruit order to this facility if it’s fully occupied.\n\nKeep track of the Bastion Defenders "
                "housed in each of your Barracks. If you lose Bastion Defenders, deduct them from your roster. Assign "
                "names and personalities to your Bastion Defenders as you see fit.")
        choice = Choice(name="Recruit: Bastion Defenders", description=desc, order_type="Recruit")
        self.choices.append(choice)
