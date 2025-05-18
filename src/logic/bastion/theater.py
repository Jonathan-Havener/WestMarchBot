from logic.bastion.choice import Choice
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

    def __init__(self, owner):
        super().__init__(owner)

        desc = ("A character can compose music or write a script for a concert or production that hasn’t started "
                "rehearsals yet. This effort takes 14 days.")
        choice = Choice(name="Conductor/Director", description=desc)
        self.choices.append(choice)

        desc = ("A character who remains in the Bastion for the entirety of the production can serve as the concert’s "
                "conductor or the production’s director.")
        choice = Choice(name="Conductor/Director", description=desc)
        self.choices.append(choice)

        desc = ("A character who remains in the Bastion for the entirety of the rehearsal period can be a star "
                "performer in one or more of the performances; one of the Theater’s hirelings can serve as an "
                "understudy for additional performances.")
        choice = Choice(name="Performer", description=desc)
        self.choices.append(choice)

        desc = ("When you issue the Empower order to this facility, its hirelings begin work on a theatrical production"
                " or concert. Rehearsals and other preparations take 14 days, followed by at least 7 days of "
                "performances. The performances can continue indefinitely until a new production gets underway.\n\nYou"
                " or another character can contribute to a production by taking one of the other options provided by"
                "this bastion.\n\nAt the end of a rehearsal period, each character who contributed to the concert or "
                "production can make a DC 15 Charisma (Performance) check. If more of these checks succeed than fail, "
                "you and any other character who contributed to the concert or production each gain a Theater die, a "
                "d6. This die changes to a d8 when you reach level 13 and a d10 when you reach level 17. At any point "
                "after the rehearsals end, a character can expend their Theater die to roll it and add the number "
                "rolled to one d20 Test they make, immediately after rolling the d20. If a character hasn’t expended "
                "their Theater die before gaining another, their first die is lost.")
        choice = Choice(name="Empower: Theatrical Event", description=desc, order_type="Empower")
        self.choices.append(choice)
