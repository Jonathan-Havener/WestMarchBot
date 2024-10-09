from .magic_manager import MagicManager
from abc import abstractmethod
import random
from .pricing_scheme import PricingScheme



from pathlib import Path
from .ansible_like import AnsibleLike


class ShopBuilder:
    def build_shops(self, directory: Path) -> list:
        this_file = Path(__file__).parent
        data_source = this_file.parent.parent / "data" / "Magic Item Distribution - Items.csv"

        magic_manager = MagicManager(source=data_source)
        price_scheme = PricingScheme()

        shops = []
        for file in directory.iterdir():
            new_shop = Shop(magic_manager, price_scheme)
            reader = AnsibleLike(source=file)
            new_shop.filter = reader.data
            new_shop.name = file.stem

            new_shop.fill_inventory()

            shops.append(new_shop)

        return shops


class Shop:
    def __init__(self, magic_manager_obj: MagicManager, price_scheme_object: PricingScheme = None):
        self._magic_man = magic_manager_obj
        self.__stock = []
        self._capacity = 5
        self.inventory = []
        if not price_scheme_object:
            price_scheme_object = PricingScheme()
        self.price_scheme = price_scheme_object

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
            raise Exception()
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
