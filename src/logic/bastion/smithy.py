from logic.bastion.choice import Choice
from logic.bastion.special_facility import SpecialFacility


class Smithy(SpecialFacility):
    level_requirement = 5
    name = "Smithy"
    prerequisite = ""
    order = "Craft"
    description = ("This Smithy contains a forge, an anvil, and other tools needed to craft weapons, armor, and other "
                   "equipment.")
    space = "Roomy"
    hirelings = 2

    def __init__(self, owner):
        super().__init__(owner)

        desc = ("The facility’s hirelings craft anything that can be made with Smith’s Tools, using the rules in the "
                "Player’s Handbook.")
        choice = Choice(name="Craft: Smith’s Tools", description=desc, order_type="Craft")
        self.choices.append(choice)

        desc = ("If you are level 9+, can you commission the facility’s hirelings to craft a Common or an Uncommon "
                "magic item chosen by you from the Armaments tables in chapter 7. The facility has the tool required "
                "to craft the item, and the hirelings have proficiency with that tool as well as proficiency in the "
                "Arcana skill. See the “Crafting Magic Items” section in chapter 7 for the time and money that must be"
                " spent to craft the item. If the item allows its user to cast any spells from it, you must craft the "
                "item yourself (the facility’s hirelings can assist), and you must have all those spells prepared "
                "every day you spend crafting the item.")
        choice = Choice(name="Craft: Magic Item (Armament)", description=desc, order_type="Craft")
        self.choices.append(choice)
