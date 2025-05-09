import unittest
from src.logic.shop_bot.shop import MagicManager
from pathlib import Path


class TestMagicManager(unittest.TestCase):
    def setUp(self):
        this_file = Path(__file__).parent
        data_source = this_file.parent.parent.parent / "data" / "dmg-magic-item-definitions.json"

        assert data_source.exists()
        self._manager = MagicManager(source=data_source)

    def test_retrieval(self):
        num_items = len(self._manager.items)
        self.assertEqual(1340, num_items)

        item_filter = {}
        items = self._manager.get_filtered_items(item_filter)
        self.assertEqual(1340, len(items))

        item_filter = {
            "rarity": ["Common", "Uncommon"]
        }
        items = self._manager.get_filtered_items(item_filter)
        self.assertEqual(394, len(items))

        item_filter = {
            "filterType": ["Weapon"],
        }
        items = self._manager.get_filtered_items(item_filter)
        self.assertEqual(621, len(items))


if __name__ == '__main__':
    unittest.main()
