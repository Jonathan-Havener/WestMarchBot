from logic.bastion.special_facility import SpecialFacility


class Library(SpecialFacility):
    level_requirement = 5
    name = "Library"
    prerequisite = ""
    order = "Research"
    description = "This Library contains a collection of books plus one or more desks and reading chairs."
    space = "Roomy"
    hirelings = 1
