from .arcane_study import ArcaneStudy
from .armory import Armory
from .gaming_hall import GamingHall
from .garden import Garden
from .greenhouse import Greenhouse
from .laboratory import Laboratory
from .library import Library
from .sacristy import Sacristy
from .scriptorium import Scriptorium
from .smithy import Smithy
from .stable import Stable
from .storehouse import Storehouse
from .teleportation_circle import TeleportationCircle
from .theater import Theater
from .training_area import TrainingArea
from .trophy_room import TrophyRoom
from .workshop import Workshop
from .special_facility import SpecialFacility


class Bastion:
    def __init__(self, owner):
        self.owner = owner

    @classmethod
    async def create(cls, owner):
        self = cls(owner)

        self.options = []
        for subclass in SpecialFacility.__subclasses__():
            facility = subclass(self.owner)
            self.options.append(facility)

        return self
