from logic.bastion.special_facility import SpecialFacility


class Theater(SpecialFacility):
    level_requirement = 9
    name = "Theater"
    prerequisite = ""
    order = "Empower"
    description = ("The Theater contains a stage, a backstage area where props and sets are kept, and a seating area "
                   "for a small audience.")
    space = "Vast"
    hirelings = 4
