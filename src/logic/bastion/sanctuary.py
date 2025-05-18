from logic.bastion.special_facility import SpecialFacility


class Sanctuary(SpecialFacility):
    level_requirement = 5
    name = "Sanctuary"
    prerequisite = "Ability to use a Holy Symbol or Druidic Focus as a Spellcasting Focus"
    order = "Craft"
    description = "Icons of your religion are displayed in this facility, which includes a quiet place for worship."
    space = "Roomy"
    hirelings = 1
