from logic.bastion.choice import Choice
from logic.bastion.special_facility import SpecialFacility


class Armory(SpecialFacility):
    level_requirement = 5
    name = "Armory"
    prerequisite = ""
    order = "Trade"
    description = ("An Armory contains mannequins for displaying armor, hooks for holding Shields, racks for storing "
                   "weapons, and chests for holding ammunition.")
    space = "Roomy"
    hirelings = 1

    def __init__(self, owner):
        super().__init__(owner)

        desc = ("When you issue the Trade order to this facility, you commission the facility’s hireling to stock the "
                "Armory with armor, Shields, weapons, and ammunition. This equipment costs you 100 GP plus an extra "
                "100 GP for each Bastion Defender in your Bastion. If your Bastion has a Smithy, the total cost is "
                "halved.\nWhile your Armory is stocked, your Bastion Defenders are harder to kill. When any event "
                "causes you to roll dice to determine if your Bastion loses one or more of its defenders (see “Bastion "
                "Events” at the end of this chapter), roll 1d8 in place of each d6 you would normally roll. When the "
                "event is over, the equipment in your Armory is expended regardless of how many Bastion Defenders you "
                "have or how many you lost, leaving your Armory depleted until you issue another Trade order to the "
                "facility and pay the cost to restock it.")
        trade_stock_armory = Choice(name="Trade: Stock Armory", description=desc, order_type="Trade",
                                    cost=100)
        self.choices.append(trade_stock_armory)
