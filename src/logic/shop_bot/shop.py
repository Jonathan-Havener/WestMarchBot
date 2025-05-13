from .magic_manager import MagicManager
import random

from pathlib import Path
import yaml


class ShopBuilder:
    def build_shops(self, directory: Path) -> list:
        this_file = Path(__file__).parent
        data_source = this_file.parent.parent.parent / "data" / "dmg-magic-item-definitions.json"

        magic_manager = MagicManager(source=data_source)

        shops = []
        for file in directory.iterdir():
            new_shop = Shop(magic_manager)

            with open(file, "r") as file_source:
                data = yaml.safe_load(file_source)
                data = data[list(data.keys())[0]]
            new_shop.filter = data
            new_shop.name = data["name"]

            new_shop.fill_inventory()

            shops.append(new_shop)

        return shops


class Shop:
    def __init__(self, magic_manager_obj: MagicManager):
        self._magic_man = magic_manager_obj
        self.__stock = []
        self._capacity = 5
        self.inventory = []

        self.filter = {}
        self.name = "Basic Shop"
        self.description = "Some shop information."

    @property
    def _stock(self) -> list:
        if not self.__stock:
            self.__stock = self._magic_man.get_filtered_items(self.filter)
        return self.__stock

    def fill_inventory(self) -> None:
        available_space = self._capacity - len(self.inventory)
        if not len(self._stock) > 0:
            return
        new_stock = random.choices(self._stock, k=available_space)

        for item in new_stock:
            self.inventory += [{
                "item": item,
                "price": self._magic_man.get_price(item)
            }]

    def sell(self, item_name: str) -> [dict, None]:
        item_index = next((i for i, listing in enumerate(self.inventory) if listing["item"]["name"] == item_name), -1)
        if item_index < 0:
            return None
        finished_listing = self.inventory.pop(item_index)
        return finished_listing
