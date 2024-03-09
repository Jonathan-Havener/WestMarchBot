from .character_database_interface import CharacterDBI, QuestDBI, MemoryDBI, ExperienceDBI, Session
from .experience import ExperienceBuilder
import logging


# This is the Originator in the Memento pattern
class Character:
    def __init__(self, name):
        self._name = name
        self._quest_name = None
        self._last_adventure_date = None
        self._alive = True
        self._has_unsaved_changes = False
        self._experiences = []

        self.session = Session()

        self.logger = logging.getLogger(str(self))
        self.build_logger()

    def __del__(self):
        self.session.close()

    def build_logger(self):
        # Create a formatter with your desired format
        formatter = logging.Formatter(f'Character: {self.name}\tQuest: {self._quest_name}\tLevel:{self.total_level}',
                                      validate=False)
        # Create a handler for writing log messages to the console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)  # Set the handler level to DEBUG
        console_handler.setFormatter(formatter)
        # Add the console handler to the logger
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.DEBUG)

    def go_on_adventure(self, quest_name, adventure_date, adventurer_messages) -> None:
        """
        This updates the character's state
        :return:
        :rtype:
        """
        if quest_name == self._quest_name:
            return
        self._has_unsaved_changes = True

        if self._last_adventure_date and adventure_date < self._last_adventure_date:
            self.logger.warning(f"{quest_name} has occurred before the last adventure {self._quest_name}")
        self._last_adventure_date = adventure_date

        new_experiences = ExperienceBuilder().build_experiences(message_history=adventurer_messages)
        new_experience_level_total = sum([experience.level for experience in new_experiences])
        if new_experience_level_total < self.total_level:
            self.logger.warning(f"Player would lose experience going on quest {quest_name}!")
        self._experiences = new_experiences
        self._quest_name = quest_name

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

    @property
    def total_level(self):
        if not self._experiences:
            return 0
        return sum([experience.level for experience in self._experiences])

    def save(self, player_name, discord_tag) -> None:
        """
        Saves the current state of the character to the database
        :return:
        :rtype:
        """
        self._has_unsaved_changes = False

        character = self.session.query(CharacterDBI).filter_by(character_name=self._name).first()
        if character:
            # There is already an entry in the database for this character so just update it
            character.character_name = self._name
            character.player_name = player_name
            character.discord_tag = discord_tag
        else:
            # This character doesn't exist yet so create it
            character = CharacterDBI(
                character_name=self._name,
                player_name=player_name,
                discord_tag=discord_tag,
            )
            self.session.add(character)

        quest = self.session.query(QuestDBI).filter_by(quest_name=self._quest_name).first()
        if not quest:
            quest = QuestDBI(
                quest_name=self._quest_name
            )
            self.session.add(quest)

        memory = MemoryDBI(
            level=0,
            alive=True,
            quest=quest,
            character=character,
        )
        self.session.add(memory)

        experience = ExperienceDBI(
            character_class="",
            subclass="",
            level=0,
            memory=memory
        )
        self.session.add(experience)

        # Commit the changes to the database
        self.session.commit()

    def restore(self, memento: CharacterDBI) -> None:
        """
        Finds the latest information from the database and recreates the class information
        :param memento:
        :type memento:
        :return:
        :rtype:
        """
        pass
