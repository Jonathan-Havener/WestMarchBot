from logic.bastion.special_facility import SpecialFacility


class Garden(SpecialFacility):
    level_requirement = 5
    name = "Garden"
    prerequisite = ""
    order = "Harvest"
    description = ("A Bastion can have more than one Garden. Each time you add a Garden to your Bastion, choose its "
                   "type from the options in the Garden Types table. While in your Bastion, you can instruct the "
                   "facility’s hireling to change the Garden from one type to another. This work takes 21 days, during"
                   " which time no other activity can occur in this facility.")
    space = "Roomy"
    hirelings = 1
