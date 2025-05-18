class Choice:
    def __init__(self, name: str, description: str,
                 order_type: str = "", craft_time=None, duration=None,
                 cost=None, level_requirement=5):
        self.name = name
        self.description = description
        self.order_type = order_type
        self.craft_time = craft_time
        self.duration = duration
        self.cost = cost
        self.level_requirement = level_requirement
