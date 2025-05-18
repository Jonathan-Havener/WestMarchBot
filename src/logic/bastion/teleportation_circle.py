from logic.bastion.special_facility import SpecialFacility


class TeleportationCircle(SpecialFacility):
    level_requirement = 9
    name = "Teleportation Circle"
    prerequisite = ""
    order = "Recruit"
    description = ("Inscribed on the floor of this room is a permanent teleportation circle created by the "
                   "Teleportation Circle spell.")
    space = "Roomy"
    hirelings = 1
