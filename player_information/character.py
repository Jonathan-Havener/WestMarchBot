from .memento import Memento
from .experience import ExperienceBuilder


# This is the Originator in the Memento pattern
class Character:
    def __init__(self, name):
        self._name = name
        self._quest_name = None
        self._last_adventure_date = None
        self._alive = True
        self._has_unsaved_changes = False
        self._experiences = []

    def go_on_adventure(self, quest_name, adventure_date, adventurer_messages) -> None:
        """
        This updates the character's state
        :return:
        :rtype:
        """
        if quest_name == self._quest_name:
            return
        self._has_unsaved_changes = True
        self._quest_name = quest_name
        self._last_adventure_date = adventure_date
        self._experiences = ExperienceBuilder().build_experiences(message_history=adventurer_messages)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, character_name) -> None:
        if character_name == self._name:
            return
        self._name = character_name

    @property
    def alive(self) -> bool:
        return self._alive

    @alive.setter
    def alive(self, status: bool) -> None:
        if status == self._alive:
            return
        self._has_unsaved_changes = True
        self._alive = status

    @property
    def has_unsaved_changes(self) -> bool:
        return self._has_unsaved_changes

    def save(self) -> Memento:
        """
        This returns an update of the players adventure
        :return:
        :rtype:
        """
        self._has_unsaved_changes = False
        return Memento()

    def restore(self, memento: Memento) -> None:
        """
        Restores the character to a previous adventuring point
        :param memento:
        :type memento:
        :return:
        :rtype:
        """
        pass
