from logic.bastion.choice import Choice
from logic.bastion.special_facility import SpecialFacility


class ArcaneStudy(SpecialFacility):
    level_requirement = 5
    name = "Arcane Study"
    prerequisite = "Ability to use an Arcane Focus or a tool as a Spellcasting Focus"
    order = "Craft"
    description = "An Arcane Study is a place of quiet research that contains one or more desks and bookshelves."
    space = "Roomy"
    hirelings = 1

    def __init__(self, owner):
        super().__init__(owner)

        desc = ("After spending a Long Rest in your Bastion, you gain a magical Charm (see “Supernatural Gifts” in "
                "chapter 3) that lasts for 7 days or until you use it. The Charm allows you to cast Identify without "
                "expending a spell slot or using Material components. You can’t gain this Charm again while you still "
                "have it.")
        arcane_study_charm = Choice(name="Arcane Study Charm", description=desc,
                                    craft_time="Long Rest", duration="7 days")
        self.choices.append(arcane_study_charm)

        desc = ("You commission the facility’s hireling to craft an Arcane Focus. The work takes 7 days and costs no "
                "money. The Arcane Focus remains in your Bastion until you claim it.")
        craft_arcane_focus = Choice(name="Craft: Arcane Focus", description=desc, order_type="Craft",
                                    craft_time="7 days")
        self.choices.append(craft_arcane_focus)

        desc = ("You commission the facility’s hireling to craft a blank book. The work takes 7 days and costs you 10 "
                "GP. The book remains in your Bastion until you claim it.")
        craft_book = Choice(name="Craft: Book", description=desc, order_type="Craft", craft_time="7 days", cost=10)
        self.choices.append(craft_book)

        # TODO : Program the costs (Maybe give multiple options for each type?)
        desc = ("If you are level 9+, you can commission the facility’s hireling to craft a Common or an Uncommon "
                "magic item chosen by you from the Arcana tables in chapter 7. The facility has the tool required to "
                "craft the item, and the hireling has proficiency with that tool as well as proficiency in the Arcana "
                "skill. See the “Crafting Magic Items” section in chapter 7 for the time and money that must be spent "
                "to craft the item. If the item allows its user to cast any spells from it, you must craft the item "
                "yourself (the facility’s hireling can assist), and you must have all those spells prepared every day "
                "you spend crafting the item.")
        craft_book = Choice(name="Craft: Magic Item (Arcana)", description=desc, order_type="Craft",
                            level_requirement=9)
        self.choices.append(craft_book)
