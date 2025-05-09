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
            new_shop.name = file.stem

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

    def get_price(self, magic_item):
        if magic_item["name"] == "Spell Scroll (Cantrip)":
            return 30
        elif magic_item["name"] == "Spell Scroll (Level 1)":
            return 50
        elif magic_item["name"] == "Spell Scroll (Level 2)":
            return 200
        elif magic_item["name"] == "Spell Scroll (Level 3)":
            return 300
        elif magic_item["name"] == "Spell Scroll (Level 4)":
            return 2000
        elif magic_item["name"] == "Spell Scroll (Level 5)":
            return 3000
        elif magic_item["name"] == "Spell Scroll (Level 6)":
            return 20000
        elif magic_item["name"] == "Spell Scroll (Level 7)":
            return 25000
        elif magic_item["name"] == "Spell Scroll (Level 8)":
            return 30000
        elif magic_item["name"] == "Spell Scroll (Level 9)":
            return 100000

        base_price = 0
        if magic_item["rarity"] == "Common":
            base_price = 100
        elif magic_item["rarity"] == "Uncommon":
            base_price = 400
        elif magic_item["rarity"] == "Rare":
            base_price = 4000
        elif magic_item["rarity"] == "Very Rare":
            base_price = 40000
        elif magic_item["rarity"] == "Legendary":
            base_price = 200000

        if magic_item["filterType"] == "Weapon":
            if magic_item["type"] == "Club":
                base_price += .1
            elif magic_item["type"] == "Dagger":
                base_price += 2
            elif magic_item["type"] == "Greatclub":
                base_price += .2
            elif magic_item["type"] == "Handaxe":
                base_price += 5
            elif magic_item["type"] == "Javelin":
                base_price += .5
            elif magic_item["type"] == "Light Hammer":
                base_price += 2
            elif magic_item["type"] == "Mace":
                base_price += 5
            elif magic_item["type"] == "Quarterstaff":
                base_price += .2
            elif magic_item["type"] == "Sickle":
                base_price += 1
            elif magic_item["type"] == "Spear":
                base_price += 1
            elif magic_item["type"] == "Dart":
                base_price += .05
            elif magic_item["type"] == "Light Crossbow":
                base_price += 25
            elif magic_item["type"] == "Shortbow":
                base_price += 25
            elif magic_item["type"] == "Sling":
                base_price += .1
            elif magic_item["type"] == "Battleaxe":
                base_price += 10
            elif magic_item["type"] == "Flail":
                base_price += 10
            elif magic_item["type"] == "Glaive":
                base_price += 20
            elif magic_item["type"] == "Greataxe":
                base_price += 30
            elif magic_item["type"] == "Greatsword":
                base_price += 50
            elif magic_item["type"] == "Halberd":
                base_price += 20
            elif magic_item["type"] == "Lance":
                base_price += 10
            elif magic_item["type"] == "Longsword":
                base_price += 15
            elif magic_item["type"] == "Maul":
                base_price += 10
            elif magic_item["type"] == "Morningstar":
                base_price += 15
            elif magic_item["type"] == "Pike":
                base_price += 5
            elif magic_item["type"] == "Rapier":
                base_price += 25
            elif magic_item["type"] == "Scimitar":
                base_price += 25
            elif magic_item["type"] == "Shortsword":
                base_price += 10
            elif magic_item["type"] == "Trident":
                base_price += 5
            elif magic_item["type"] == "Warhammer":
                base_price += 15
            elif magic_item["type"] == "War Pick":
                base_price += 5
            elif magic_item["type"] == "Whip":
                base_price += 2
            elif magic_item["type"] == "Blowgun":
                base_price += 10
            elif magic_item["type"] == "Hand Crossbow":
                base_price += 75
            elif magic_item["type"] == "Heavy Crossbow":
                base_price += 40
            elif magic_item["type"] == "Longbow":
                base_price += 40

        if magic_item["filterType"] == "Armor":
            if magic_item["baseArmorName"] == "Padded":
                base_price += 5
            elif magic_item["baseArmorName"] == "Leather":
                base_price += 10
            elif magic_item["baseArmorName"] == "Studded Leather":
                base_price += 40
            elif magic_item["baseArmorName"] == "Hide":
                base_price += 10
            elif magic_item["baseArmorName"] == "Chain Shirt":
                base_price += 50
            elif magic_item["baseArmorName"] == "Scale Mail":
                base_price += 50
            elif magic_item["baseArmorName"] == "Breastplate":
                base_price += 400
            elif magic_item["baseArmorName"] == "Half Plate":
                base_price += 750
            elif magic_item["baseArmorName"] == "Ring Mail":
                base_price += 30
            elif magic_item["baseArmorName"] == "Chain Mail":
                base_price += 75
            elif magic_item["baseArmorName"] == "Splint":
                base_price += 200
            elif magic_item["baseArmorName"] == "Plate":
                base_price += 1500
            elif magic_item["baseArmorName"] == "Shield":
                base_price += 10

        if magic_item["isConsumable"]:
            base_price = base_price / 2

        return base_price

    def fill_inventory(self) -> None:
        available_space = self._capacity - len(self.inventory)
        if not len(self._stock) > 0:
            raise Exception()
        new_stock = random.choices(self._stock, k=available_space)

        for item in new_stock:
            self.inventory += [{
                "item": item,
                "price": self.get_price(item)
            }]

    def sell(self, item_name: str) -> [dict, None]:
        item_index = next((i for i, listing in enumerate(self.inventory) if listing["item"]["name"] == item_name), -1)
        if item_index < 0:
            return None
        finished_listing = self.inventory.pop(item_index)
        return finished_listing
