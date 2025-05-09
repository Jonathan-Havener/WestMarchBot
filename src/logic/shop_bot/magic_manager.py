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
                property in item and item[property] in item_filter[property]
                for property in item_filter]
            )
        ]
        return filtered_items
