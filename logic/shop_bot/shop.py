from .magic_item import MagicItem
from .magic_manager import MagicManager
from abc import abstractmethod
from pathlib import Path
import yaml
import random


class PricingScheme:
    def __init__(self, source: [Path] = None):
        self.data = {}
        self.rarity = None
        self.impact = None
        if not source:
            source = Path(__file__).parent.parent.parent / "data" / "magic_item_prices.yml"
        self._load_properties(source)

    @property
    def _num_dice(self):
        return self.data[self.rarity][self.impact]["num_dice"]

    @property
    def _dice_face(self):
        return self.data[self.rarity][self.impact]["dice_face"]

    @property
    def _adder(self):
        return self.data[self.rarity][self.impact]["adder"]

    @property
    def _multiplier(self):
        return self.data[self.rarity][self.impact]["multiplier"]

    def _merge_properties(self, data):
        # This function will merge properties from parents to children
        if isinstance(data, dict):
            for key, value in data.items():
                # Recursively merge properties of subkeys
                data[key] = self._merge_properties(value)
            if "child_key" in data:
                other_data = {key: data[key] for key in data if key != "child_key"}
                data = {
                    child: data["child_key"][child]
                    for child in data["child_key"].keys()
                }
                for key in data:
                    data[key].update(other_data)
        return data

    def _load_properties(self, filename):
        with open(filename, 'r') as file:
            self.data = yaml.safe_load(file) # Load YAML file
            self.data = self.data["items"]
            self.data = self._merge_properties(self.data)

    def get_price(self, magic_item):
        self.rarity = magic_item.rarity.lower().replace(" ", "_")
        self.impact = magic_item.impact.lower()

        return (sum(
            [random.randint(1, self._dice_face)
             for i in range(0, self._num_dice)]
        ) + self._adder) * self._multiplier


class Shop:
    def __init__(self, magic_manager_obj: MagicManager, price_scheme_object: PricingScheme= None):
        self._magic_man = magic_manager_obj
        self.__stock = []
        self._capacity = 5
        self.inventory = []
        if not price_scheme_object:
            price_scheme_object = PricingScheme()
        self.price_scheme = price_scheme_object

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
            item.add_supplier(self)

            self.inventory += [{
                "item": item,
                "price": self.price_scheme.get_price(item)
            }]

    def sell(self, item_name: str) -> [dict, None]:
        item_index = next((i for i, listing in enumerate(self.inventory) if listing["item"].name == item_name), -1)
        if item_index < 0:
            return None
        finished_listing = self.inventory.pop(item_index)
        return finished_listing
