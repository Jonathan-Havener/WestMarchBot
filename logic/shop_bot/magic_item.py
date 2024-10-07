class MagicItem:
    def __init__(self,
                 name: str,
                 rarity: str,
                 item_type: str,
                 attune: str,
                 impact: str
                 ):
        self.name = name
        self.rarity = rarity
        self.item_type = item_type
        self.attunement = attune
        self.impact = impact

        self.suppliers = []
