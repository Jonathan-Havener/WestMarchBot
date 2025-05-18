from logic.bastion.choice import Choice
from logic.bastion.special_facility import SpecialFacility


class Garden(SpecialFacility):
    level_requirement = 5
    name = "Garden"
    prerequisite = ""
    order = "Harvest"
    description = ("A Bastion can have more than one Garden. Each time you add a Garden to your Bastion, choose its "
                   "type from the options in the Garden Types table. While in your Bastion, you can instruct the "
                   "facility’s hireling to change the Garden from one type to another. This work takes 21 days, during"
                   " which time no other activity can occur in this facility.")
    space = "Roomy"
    hirelings = 1

    def __init__(self, owner):
        super().__init__(owner)
        # TODO: Create table

        desc = ("You can enlarge your Garden to a Vast facility by spending 2,000 GP. A Vast Garden is equivalent to "
                "two Roomy Gardens and can include two of the same type of Garden or two different types. When you "
                "issue the Harvest order to a Vast Garden, each component garden produces its own harvest. A Vast "
                "Garden gains one additional hireling.")
        choice = Choice(name="Enlarging the Facility", description=desc, cost=2000)
        self.choices.append(choice)

        desc = ("When you issue the Harvest order to this facility, you commission the facility’s hireling to collect "
                "items from the Garden as noted in the Garden Types table. The work takes 7 days and costs no money.")
        choice = Choice(name="Harvest: Garden Growth", description=desc, order_type="Harvest", craft_time="7 days")
        self.choices.append(choice)
