from pathlib import Path
import json


class MagicManager:
    """
    Creates Magic Items from a data source and provides item filtering
    """
    def __init__(self, source: Path):
        with open(source, "r", encoding='utf-8') as file:
            self.items = json.load(file)

    def get_filtered_items(self, item_filter: dict):
        filtered_items = [
            item
            for item in self.items
            if all([
                property in item and item[property] in item_filter.get("keyParams", []).get(property,[])
                for property in item_filter.get("keyParams", [])
                if item_filter.get("keyParams",[]).get(property, None)
            ])
        ]
        # Filter by item name contains
        items = [
            item
            for item in filtered_items
            if item_filter.get("itemText", "").lower() in item["name"].lower()
        ]
        return items

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
