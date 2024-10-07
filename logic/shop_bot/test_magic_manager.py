import unittest
from logic.shop_bot.shop import MagicManager
from pathlib import Path


class TestMagicManager(unittest.TestCase):
    def setUp(self):
        this_file = Path(__file__).parent
        data_source = this_file.parent.parent / "data" / "Magic Item Distribution - Items.csv"

        assert data_source.exists()
        self._manager = MagicManager(source=data_source)

    def test_retrieval(self):
        num_items = len(self._manager.items)
        self.assertEqual(378, num_items)

        item_filter = {}
        items = self._manager.get_filtered_items(item_filter)
        self.assertEqual(378, len(items))

        item_filter = {
            "impact": ["Minor"],
            "rarity": ["Common", "Uncommon"]
        }
        items = self._manager.get_filtered_items(item_filter)
        self.assertEqual(91, len(items))

        item_filter = {
            "item_type": ["Weapon"],
        }
        items = self._manager.get_filtered_items(item_filter)
        self.assertEqual(39, len(items))


if __name__ == '__main__':
    unittest.main()
