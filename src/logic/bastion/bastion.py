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
        self.facilities = {
            "all": set(),
            "owned": set()
        }

    @classmethod
    async def create(cls, owner):
        self = cls(owner)

        for subclass in SpecialFacility.__subclasses__():
            facility = subclass(self.owner)
            self.facilities["all"].add(facility)

        return self

    async def _get_num_facilities_needing_construction(self):
        num_special_allowed = 0
        char_level = await self.owner.level()
        if char_level >= 5:
            num_special_allowed += 2
        if char_level >= 9:
            num_special_allowed += 2
        num_left = num_special_allowed - len(self.facilities["owned"])
        return num_left

    async def get_available_facilities(self) -> []:
        num_needed = await self._get_num_facilities_needing_construction()

        if num_needed <= 0:
            return []

        char_level = await self.owner.level()

        available_facilities = set()
        for facility in self.facilities["all"]:
            if char_level < facility.level_requirement:
                continue
            if facility in self.facilities["owned"]:
                continue
            available_facilities.add(facility)

        return available_facilities
