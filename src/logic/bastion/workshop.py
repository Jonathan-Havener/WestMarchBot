from logic.bastion.choice import Choice
from logic.bastion.special_facility import SpecialFacility


class Workshop(SpecialFacility):
    level_requirement = 5
    name = "Workshop"
    prerequisite = ""
    order = "Craft"
    description = ("This Workshop is a creative space where useful items can be crafted. The Workshop comes equipped "
                   "with six different kinds of Artisan’s Tools, chosen from the following list: Carpenter’s Tools, "
                   "Cobbler’s Tools, Glassblower’s Tools, Jeweler’s Tools, Leatherworker’s Tools, Mason’s Tools, "
                   "Painter’s Tools, Potter’s Tools, Tinker’s Tools, Weaver’s Tools, Woodcarver’s Tools")
    space = "Roomy"
    hirelings = 3

    def __init__(self, owner):
        super().__init__(owner)

        desc = ("After spending an entire Short Rest in your Workshop, you gain Heroic Inspiration. You can’t gain this"
                " benefit again until you finish a Long Rest.")
        choice = Choice(name="Source of Inspiration", description=desc)
        self.choices.append(choice)

        desc = ("You can enlarge your Workshop to a Vast facility by spending 2,000 GP. If you do so, the Workshop "
                "gains two additional hirelings and three additional Artisan’s Tools (chosen from the list above).")
        choice = Choice(name="Enlarging the Facility", description=desc, cost=2000)
        self.choices.append(choice)

        desc = ("The facility’s hirelings craft anything that can be made with the tools you chose when you added the "
                "Workshop to your Bastion (see above), using the rules in the Player’s Handbook.")
        choice = Choice(name="Craft: Adventuring Gear", description=desc, order_type="Craft")
        self.choices.append(choice)

        desc = ("If you are level 9+, you can commission the facility’s hirelings to craft a Common or an Uncommon "
                "magic item chosen by you from the Implements tables in chapter 7. The facility has the tool required"
                " to craft the item, and the hirelings have proficiency with that tool as well as proficiency in the "
                "Arcana skill. See the “Crafting Magic Items” section in chapter 7 for the time and money that must be "
                "spent to craft the item. If the item allows its user to cast any spells from it, you must craft the "
                "item yourself (the facility’s hirelings can assist), and you must have all those spells prepared every"
                " day you spend crafting the item.")
        choice = Choice(name="Craft: Magic Item (Implement)", description=desc, order_type="Craft")
        self.choices.append(choice)
