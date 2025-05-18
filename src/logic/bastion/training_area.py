from logic.bastion.special_facility import SpecialFacility


class TrainingArea(SpecialFacility):
    level_requirement = 9
    name = "Training Area"
    prerequisite = ""
    order = "Empower"
    description = ("A Bastion can have more than one Training Area. A Training Area might be an open courtyard, a "
                   "gymnasium, a music or dance hall, or a cleverly built gauntlet of traps and hazards. It might "
                   "contain inanimate targets (for weapon practice), padded mats, and other equipment. One of the "
                   "facility’s hirelings is an expert trainer; the others serve as training partners. When a Training "
                   "Area becomes part of your Bastion, choose one trainer from the Expert Trainers table. On each "
                   "Bastion turn, you can replace that trainer with another one from the table.")
    space = "Vast"
    hirelings = 4
