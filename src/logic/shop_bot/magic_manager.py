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
