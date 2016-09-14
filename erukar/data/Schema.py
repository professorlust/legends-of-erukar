from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class EquippedItem(Base):
    __tablename__ = 'equippeditems'

    character_id    = Column(Integer, ForeignKey('characters.id'), primary_key=True)
    item_id         = Column(Integer, ForeignKey('items.id'), primary_key=True)
    item            = relationship("Item")
    equipment_slot  = Column(String)


class Player(Base):
    __tablename__ = 'players'

    id          = Column(Integer, primary_key=True)
    uid         = Column(String, nullable=False)
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
    level       = Column(Integer)
    experience  = Column(Integer)

    equipment   = relationship("EquippedItem")
    inventory   = relationship("Item")
    effects     = relationship("Effect")
    player_id   = Column(Integer, ForeignKey('players.id'), nullable=False)
    player      = relationship("Player", foreign_keys=[player_id])


class Item(Base):
    __tablename__ = 'items'

    id              = Column(Integer, primary_key=True)
    item_type       = Column(String)
    character_id    = Column(Integer, ForeignKey('characters.id'))
    character       = relationship("Character", foreign_keys=[character_id])
    material_class  = Column(String)
    modifiers       = relationship("Modifier")


class Modifier(Base):
    __tablename__ = 'modifiers'

    id              = Column(Integer, primary_key=True)
    modifier_type   = Column(String)
    item_id         = Column(Integer, ForeignKey('items.id'))
    item            = relationship("Item", foreign_keys=[item_id])


class Effect(Base):
    __tablename__ = 'effects'

    id              = Column(Integer, primary_key=True)
    effect_type     = Column(String)
    character_id    = Column(Integer, ForeignKey('characters.id'))
    character       = relationship("Character", foreign_keys=[character_id])
