from pathlib import Path
from .ansible_like import AnsibleLike
import random


class PricingScheme(AnsibleLike):
    def __init__(self, source: [Path] = None):
        self.data = {}
        self.rarity = None
        self.impact = None
        if not source:
            source = Path(__file__).parent.parent.parent / "data" / "magic_item_prices.yml"
        super().__init__(source)
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

    def get_price(self, magic_item):
        self.rarity = magic_item.rarity.lower().replace(" ", "_")
        self.impact = magic_item.impact.lower()

        return (sum(
            [random.randint(1, self._dice_face)
             for i in range(0, self._num_dice)]
        ) + self._adder) * self._multiplier
