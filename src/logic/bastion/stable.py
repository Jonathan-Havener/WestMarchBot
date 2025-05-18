from logic.bastion.special_facility import SpecialFacility


class Stable(SpecialFacility):
    level_requirement = 9
    name = "Stable"
    prerequisite = ""
    order = "Trade"
    description = ("A Bastion can have more than one Stable. Each Stable you add to your Bastion comes with one Riding"
                   " Horse or Camel and two Ponies or Mules; see the Player’s Handbook or the Monster Manual for these"
                   " creatures’ stat blocks. The facility is big enough to house three Large animals. Two Medium "
                   "creatures occupy the same amount of space as one Large creature there. The facility’s hireling "
                   "looks after these creatures. After a Beast that can serve as a mount spends at least 14 days in "
                   "this facility, all Wisdom (Animal Handling) checks made with respect to it have Advantage.")
    space = "Roomy"
    hirelings = 1
