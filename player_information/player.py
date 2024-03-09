from .character import Character
import logging


# This is the caretaker part of the Memento pattern
class Player:
    table = "players"

    def __init__(self) -> None:
        self.player_name = None
        self.discord_tag = None
        # originator : memento
        self._characters = {}

    def add_character(self, character: Character) -> None:
        if character.name in [self._characters[pc]["obj"].name for pc in self._characters]:
            logging.debug(f"Tried adding {character.name} to {self.player_name or self.discord_tag} but that character "
                          f"already exists!")
            return
        self._characters.update({
            character.name: {
                "obj": character,
                "history": []
            }
        })

    def get_character(self, name):
        matched_characters = [self._characters[character]["obj"] for character in self._characters
                              if self._characters[character]["obj"] == name]
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
            if self._characters[character]["obj"].has_unsaved_changes:
                character_memento = self._characters[character]["obj"].save(self.player_name, self.discord_tag)
                self._characters[character]["history"].append(character_memento)

    def show_history(self) -> None:
        """
        This displays all the player's history
        :return:
        :rtype:
        """
        from .character_database_interface import CharacterDBI, QuestDBI, MemoryDBI, ExperienceDBI, Session
        session = Session()
        characters = session.query(CharacterDBI).all()
        print(characters)
        session.commit()
        session.close()
