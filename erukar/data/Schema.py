from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'

    id          = Column(Integer, primary_key=True)
    uid         = Column(String)
    name        = Column(String)
    characters  = relationship("Character")


class Character(Base):
    __tablename__ = 'characters'

    id          = Column(Integer, primary_key=True)
    name        = Column(String)
    max_health  = Column(Integer)
    health      = Column(Integer)
    strength    = Column(Integer)
    dexterity   = Column(Integer)
    vitality    = Column(Integer)
    acuity      = Column(Integer)
    sense       = Column(Integer)
    resolve     = Column(Integer)
    left        = Column(String)
    right       = Column(String)
    chest       = Column(String)
    head        = Column(String)
    feet        = Column(String)
    arms        = Column(String)
    legs        = Column(String)
    ring        = Column(String)
    amulet      = Column(String)
    blessing    = Column(String)
    level       = Column(Integer)
    experience  = Column(Integer)
    inventory   = relationship("Item")
    effects     = relationship("Effect")
    player_id   = Column(Integer, ForeignKey('players.id'))


class Item(Base):
    __tablename__ = 'items'

    id              = Column(Integer, primary_key=True)
    name            = Column(String)
    character_id    = Column(Integer, ForeignKey('characters.id'))
    material_class  = Column(String)
    modifiers       = relationship("Modifier")


class Modifier(Base):
    __tablename__ = 'modifiers'

    id          = Column(Integer, primary_key=True)
    class_name  = Column(String)
    item_id     = Column(Integer, ForeignKey('items.id'))


class Effect(Base):
    __tablename__ = 'effects'

    id              = Column(Integer, primary_key=True)
    class_name      = Column(String)
    character_id    = Column(Integer, ForeignKey('characters.id'))
