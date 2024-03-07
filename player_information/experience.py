import re
from itertools import zip_longest


class Experience:
    def __init__(self, level, player_class=None, subclass=None):
        self.level = level
        self.player_class = player_class
        self.subclass = subclass


# Factory method that determines a players level and class from a list of messages
class ExperienceBuilder:
    def build_experiences(self, message_history) -> list:
        inferred_classes = []

        data = self._parse_player_information(message_history)
        data = self._validate_class_information(data)
        for player_class, player_subclass, level in data:
            inferred_classes.append(
                Experience(level=level,
                           player_class=player_class,
                           subclass=player_subclass)
            )
        return inferred_classes

    def _parse_player_information(self, msg_list) -> list:
        player_classes = []
        player_subclasses = []
        levels = []

        for msg in msg_list:
            levels = levels + self._read_levels_from_msg(msg)
            player_classes = player_classes + self._read_classes_from_msg(msg)
            player_subclasses = player_subclasses + self._read_subclasses_from_msg(msg)

        information = zip_longest(player_classes, player_subclasses, levels)
        return list(information)

    @staticmethod
    def _read_levels_from_msg(msg):
        level_pattern = r"le?ve?l ?(?P<level>\d)"

        if not msg["content"]:
            return []

        res = re.findall(level_pattern, msg["content"], re.IGNORECASE)
        if res:
            levels = [int(num) for num in res]
            return levels

        return []

    @staticmethod
    def _read_classes_from_msg(msg):
        return []

    @staticmethod
    def _read_subclasses_from_msg(msg):
        return []

    @staticmethod
    def _validate_class_information(data) -> list:
        """
        This method will reallign subclasses with their associated classes
        Additionally, it should provide a class if a subclass is listed without its matching class
        :param data:
        :type data:
        :return:
        :rtype:
        """
        return data
