from logic.bastion.choice import Choice
from logic.bastion.special_facility import SpecialFacility


class Sanctuary(SpecialFacility):
    level_requirement = 5
    name = "Sanctuary"
    prerequisite = "Ability to use a Holy Symbol or Druidic Focus as a Spellcasting Focus"
    order = "Craft"
    description = "Icons of your religion are displayed in this facility, which includes a quiet place for worship."
    space = "Roomy"
    hirelings = 1

    def __init__(self, owner):
        super().__init__(owner)

        desc = ("After spending a Long Rest in your Bastion, you gain a magical Charm (see “Supernatural Gifts” in "
                "chapter 3) that lasts for 7 days or until you use it. The Charm allows you to cast Healing Word once "
                "without expending a spell slot. You can’t gain this Charm again while you still have it.")
        choice = Choice(name="Sanctuary Charm", description=desc)
        self.choices.append(choice)

        desc = ("When you issue the Craft order to this facility, you commission the facility’s hireling to craft a "
                "Druidic Focus (wooden staff) or a Holy Symbol. The work takes 7 days and costs no money. The item "
                "remains in your Bastion until you claim it.")
        choice = Choice(name="Craft: Sacred Focus", description=desc, order_type="Craft")
        self.choices.append(choice)
