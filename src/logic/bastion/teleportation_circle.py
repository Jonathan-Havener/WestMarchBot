from logic.bastion.choice import Choice
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

    def __init__(self, owner):
        super().__init__(owner)

        desc = ("Each time you issue the Recruit order to this facility, its hireling extends an invitation to a "
                "Friendly NPC spellcaster. Roll any die. If the number rolled is odd, the invitee declines the "
                "invitation, and you gain no benefit from having issued the order. If the number rolled is even, the "
                "invitee accepts the invitation and arrives in your Bastion via your Teleportation Circle.\n\nWhile "
                "you are in your Bastion, you can ask the spellcaster to cast one Wizard spell of level 4 or lower; if"
                " you are level 17+, the spell’s maximum level increases to 8. The spellcaster is assumed to have the "
                "spell prepared. If the spell has one or more Material components that cost money, you must pay for "
                "them before the spell can be cast.\n\nThe spellcaster stays for 14 days or until they cast a spell "
                "for you. The spellcaster won’t defend your Bastion and departs immediately if the Bastion is attacked"
                " (see “Bastion Events” at the end of the chapter).")
        choice = Choice(name="Recruit: Spellcaster", description=desc, order_type="Recruit")
        self.choices.append(choice)
