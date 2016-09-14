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
    left        = Column(Integer, ForeignKey('items.id'))
    right       = Column(Integer, ForeignKey('items.id'))
    chest       = Column(Integer, ForeignKey('items.id'))
    head        = Column(Integer, ForeignKey('items.id'))
    feet        = Column(Integer, ForeignKey('items.id'))
    arms        = Column(Integer, ForeignKey('items.id'))
    legs        = Column(Integer, ForeignKey('items.id'))
    ring        = Column(Integer, ForeignKey('items.id'))
    amulet      = Column(Integer, ForeignKey('items.id'))
    blessing    = Column(Integer, ForeignKey('items.id'))
    level       = Column(Integer)
    experience  = Column(Integer)
    inventory   = relationship("Item")
    effects     = relationship("Effect")
    player_id   = Column(Integer, ForeignKey('players.id'))


class Item(Base):
    __tablename__ = 'items'

    id              = Column(Integer, primary_key=True)
    item_type       = Column(String)
    character_id    = Column(Integer, ForeignKey('characters.id'))
    material_class  = Column(String)
    modifiers       = relationship("Modifier")


class Modifier(Base):
    __tablename__ = 'modifiers'

    id              = Column(Integer, primary_key=True)
    modifier_type   = Column(String)
    item_id         = Column(Integer, ForeignKey('items.id'))


class Effect(Base):
    __tablename__ = 'effects'

    id              = Column(Integer, primary_key=True)
    effect_type     = Column(String)
    character_id    = Column(Integer, ForeignKey('characters.id'))
