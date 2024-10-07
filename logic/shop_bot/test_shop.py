import unittest
from logic.shop_bot.shop import MagicManager, Shop, MagicItem
from pathlib import Path


class TestShop(unittest.TestCase):
    def setUp(self):
        this_file = Path(__file__).parent
        data_source = this_file.parent.parent / "data" / "Magic Item Distribution - Items.csv"

        assert data_source.exists()
        manager = MagicManager(source=data_source)
        self._shop = Shop(magic_manager_obj=manager)

    def test_fill_inventory(self):
        self.assertEqual(0, len(self._shop.inventory))

        self._shop.fill_inventory()
        self.assertEqual(self._shop._capacity, len(self._shop.inventory))

        self._shop.fill_inventory()
        self.assertEqual(self._shop._capacity, len(self._shop.inventory))

    def test_sell(self):
        self._shop.fill_inventory()
        starting_inventory_num = len(self._shop.inventory)
        starting_item_list = [item.name for item in self._shop.inventory]

        some_item = self._shop.inventory[0]
        num_some_item = self._shop.inventory.count(some_item)

        self._shop.sell(some_item.name)
        # The total number of items is 1 less
        self.assertEqual(starting_inventory_num-1, len(self._shop.inventory))
        # The number of this specific item is one less
        self.assertEqual(num_some_item-1, self._shop.inventory.count(some_item))


if __name__ == '__main__':
    unittest.main()
