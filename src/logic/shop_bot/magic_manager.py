from pathlib import Path
import csv
from .magic_item import MagicItem


class MagicManager:
    def __init__(self, source: Path):
        with open(source, "r") as file:
            self.items = [
                MagicItem(
                    name=row["Item"],
                    rarity=row["Rarity"],
                    item_type=row["Type"],
                    attune=row["Attune?"],
                    impact=row["Impact"]
                )
                for row in csv.DictReader(file)
            ]

    def get_filtered_items(self, item_filter: dict):
        all_items = self.items
        filtered_items = [
            item
            for item in all_items
            if all([
                hasattr(item, member_variable) and getattr(item, member_variable) in item_filter[member_variable]
                for member_variable in item_filter]
            )
        ]
        return filtered_items