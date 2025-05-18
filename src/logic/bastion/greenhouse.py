from logic.bastion.choice import Choice
from logic.bastion.special_facility import SpecialFacility


class Greenhouse(SpecialFacility):
    level_requirement = 9
    name = "Greenhouse"
    prerequisite = ""
    order = "Harvest"
    description = "A Greenhouse is an enclosure where rare plants and fungi are nurtured in a controlled climate."
    space = "Roomy"
    hirelings = 1

    def __init__(self, owner):
        super().__init__(owner)

        desc = ("One plant in your Greenhouse has three magical fruits growing on it. Any creature that eats one of "
                "these fruits gains the benefit of a Lesser Restoration spell. Fruits that aren’t eaten within 24 "
                "hours of being picked lose their magic. The plant replaces all picked fruits daily at dawn, and it "
                "can’t be transplanted without killing it.")
        choice = Choice(name="Fruit of Restoration", description=desc)
        self.choices.append(choice)

        desc = ("One plant in your Greenhouse has three magical fruits growing on it. Any creature that eats one of "
                "these fruits gains the benefit of a Lesser Restoration spell. Fruits that aren’t eaten within 24 "
                "hours of being picked lose their magic. The plant replaces all picked fruits daily at dawn, and it "
                "can’t be transplanted without killing it.")
        choice = Choice(name="Harvest: Healing Herbs", description=desc, order_type="Harvest")
        self.choices.append(choice)

        desc = ("You commission the facility’s hireling to extract one application of a poison from rare plants or "
                "fungi. Choose the type of poison from the following options: Assassin’s Blood, Malice, Pale Tincture,"
                " or Truth Serum. See “Poison” in chapter 3 for each poison’s effect. Once harvested, the poison can "
                "be contained in a vial. The work takes 7 days and costs no money.")
        choice = Choice(name="Harvest: Healing Herbs", description=desc, order_type="Harvest")
        self.choices.append(choice)
