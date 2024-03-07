from .character import Character
import logging

# This is the caretaker part of the Memento pattern
class Player:
    def __init__(self) -> None:
        self.player_name = None
        self.discord_tag = None
        # These are the originators
        self._characters = []
        # These are the mementos
        self._adventure_history = []

    def add_character(self, character: Character) -> None:
        if character.name in [pc.name for pc in self._characters]:
            logging.debug(f"Tried adding {character.name} to {self.player_name or self.discord_tag} but that character "
                          f"already exists!")
            return
        self._characters.append(character)

    def get_character(self, name):
        matched_characters=[character for character in self._characters if character.name == name]
        if matched_characters:
            return matched_characters[0]
        return None

    def backup(self) -> None:
        """
        Saves the state of a character
        :return:
        :rtype:
        """
        for character in self._characters:
            if character.has_unsaved_changes:
                self._adventure_history.append(character.save())

    def show_history(self) -> None:
        """
        This displays all the player's history
        :return:
        :rtype:
        """
        for adventure in self._adventure_history:
            print(adventure)


