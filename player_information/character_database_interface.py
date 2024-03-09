from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Create a database engine
engine = create_engine('sqlite+pysqlite:///west_march.db')

# Define a base class for our declarative class definitions
Base = declarative_base()


def func(self):
    from pprint import pformat
    return pformat(vars(self), indent=4, width=1) + "\n"


Base.__repr__ = func


class CharacterDBI(Base):
    __tablename__ = "character"

    character_name = Column(String, primary_key=True)
    player_name = Column(String)
    discord_tag = Column(String)

    memory = relationship("MemoryDBI", back_populates="character")


class QuestDBI(Base):
    __tablename__ = "quest"
    quest_name = Column(String, primary_key=True)
    memory = relationship("MemoryDBI", back_populates="quest")


class MemoryDBI(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(Integer)
    alive = Column(Boolean)
    character_name = Column(Integer, ForeignKey('character.character_name'))
    quest_name = Column(Integer, ForeignKey('quest.quest_name'))

    quest = relationship("QuestDBI", back_populates="memory")
    character = relationship("CharacterDBI", back_populates="memory")
    experience = relationship("ExperienceDBI", back_populates="memory")


class ExperienceDBI(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True, autoincrement=True)
    character_class = Column(String)
    subclass = Column(String)
    level = Column(Integer)
    memory_id = Column(Integer, ForeignKey('memory.id'))
    memory = relationship("MemoryDBI", back_populates="experience")


# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)


def add_memory_to_database(self) -> None:
    """

    :param memory:
    :type memory:
    :return:
    :rtype:
    """
    # 1) Check if this memory has a character to reference
    # 1a) If the character table isn't created, create it.
    # 1b) If the character is not in the character table, create it

    # 2) Check if there is a quest to associate this memory with
    # 2a) If the quest table isn't created yet, create it
    # 2b) If the quest isn't in the table, create it

    # 3) Create the memory

    # 4) Create the experience
    pass
