from .magic_item import MagicItem
from .magic_manager import MagicManager
from abc import abstractmethod
import random


class Shop:
    def __init__(self, magic_manager_obj: MagicManager):
        self._magic_man = magic_manager_obj
        self.__stock = []
        self._capacity = 5
        self.inventory = []

    @property
    @abstractmethod
    def _filter(self):
        return {}

    @property
    def _stock(self) -> list:
        if not self.__stock:
            self.__stock = self._magic_man.get_filtered_items(self._filter)
        return self.__stock

    def fill_inventory(self) -> None:
        available_space = self._capacity - len(self.inventory)
        new_stock = random.choices(self._stock, k=available_space)

        for item in new_stock:
            item.suppliers += [self]

        self.inventory += new_stock

    def sell(self, item_name: str) -> [MagicItem, None]:
        item_index = next((i for i, item in enumerate(self.inventory) if item.name == item_name), -1)
        if item_index < 0:
            return None
        self.inventory.pop(item_index)
