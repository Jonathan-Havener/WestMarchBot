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
