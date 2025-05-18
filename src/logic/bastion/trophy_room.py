from logic.bastion.choice import Choice
from logic.bastion.special_facility import SpecialFacility


class TrophyRoom(SpecialFacility):
    level_requirement = 9
    name = "Trophy Room"
    prerequisite = ""
    order = "Research"
    description = ("This room houses a collection of mementos, such as weapons from old battles, the mounted heads of "
                   "slain creatures, trinkets plucked from dungeons and ruins, and trophies passed down from "
                   "ancestors.")
    space = "Roomy"
    hirelings = 1

    def __init__(self, owner):
        super().__init__(owner)

        desc = ("You commission the facility’s hireling to research a topic of your choice. The topic can be a legend,"
                " any kind of creature, or a famous object. The topic need not be directly related to items on display"
                " in the room, as the trophies provide clues to research a wide variety of other subjects. The work "
                "takes 7 days. When the research concludes, the hireling obtains up to three accurate pieces of "
                "information about the topic that were previously unknown to you and shares this knowledge with you "
                "the next time you speak with them. The DM determines what information is learned.")
        choice = Choice(name="Research: Lore", description=desc, order_type="Research")
        self.choices.append(choice)

        desc = ("You commission the facility’s hireling to search for a trinket that might be of use to you. The work "
                "takes 7 days. When the research concludes, roll any die. If the number rolled is odd, the hireling "
                "finds nothing useful. If the number rolled is even, the hireling finds a magic item. Roll on the "
                "Implements—Common table in chapter 7 to determine what it is.")
        choice = Choice(name="Research: Trinket Trophy", description=desc, order_type="Research")
        self.choices.append(choice)
