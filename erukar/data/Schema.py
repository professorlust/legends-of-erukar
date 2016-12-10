from sqlalchemy.ext.declarative import declarative_base, ConcreteBase
from sqlalchemy import Column, Float, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, JSON

Base = declarative_base()

class EquippedItem(Base):
    __tablename__ = 'equippeditems'

    lifeform_id     = Column(Integer, ForeignKey('lifeforms.id'), primary_key=True)
    item_id         = Column(Integer, ForeignKey('items.id'), primary_key=True)
    item            = relationship("Item")
    equipment_slot  = Column(String)


class Player(Base):
    __tablename__ = 'players'

    id          = Column(Integer, primary_key=True)
    uid         = Column(String, nullable=False)
    name        = Column(String)
    characters  = relationship("Character")


class Lifeform(Base):
    __tablename__ = 'lifeforms'
    __mapper_args_ = { 
        'polymorphic_identity': 'lifeforms',
        'polymorphic_on': type
    }

    id          = Column(Integer, primary_key=True)
    type        = Column(String(50))
    deceased    = Column(Boolean, default=False)
    max_health  = Column(Integer, default=4)
    name        = Column(String,  default="unnamed")
    health      = Column(Integer, default=4)
    strength    = Column(Integer, default=0)
    dexterity   = Column(Integer, default=0)
    vitality    = Column(Integer, default=0)
    acuity      = Column(Integer, default=0)
    sense       = Column(Integer, default=0)
    resolve     = Column(Integer, default=0)

    level       = Column(Integer, default=1)
    experience  = Column(Integer, default=0)

    equipment   = relationship("EquippedItem", cascade="all, delete-orphan")
    inventory   = relationship("Item", cascade="all, delete-orphan")
    effects     = relationship("Effect", cascade="all, delete-orphan")


class Creature(Lifeform):
    __tablename__ = 'creatures'
    __mapper_args_ = { 
        'polymorphic_identity': 'creatures',
    }

    id          = Column(Integer, ForeignKey('lifeforms.id'), primary_key=True)
    uid         = Column(String, nullable=False)
    str_ratio   = Column(Float, default=0.1667)
    dex_ratio   = Column(Float, default=0.1667)
    vit_ratio   = Column(Float, default=0.1667)
    acu_ratio   = Column(Float, default=0.1667)
    sen_ratio   = Column(Float, default=0.1667)
    res_ratio   = Column(Float, default=0.1667)
    elite_points= Column(Float, default=0.0)

    template    = Column(String, nullable=False)
    modifiers   = Column(ARRAY(String))
    history     = Column(ARRAY(String))
    region      = Column(String)


class Character(Lifeform):
    __tablename__ = 'characters'
    __mapper_args_ = { 
        'polymorphic_identity': 'characters',
    }

    id          = Column(Integer, ForeignKey('lifeforms.id'), primary_key=True)
    stat_points = Column(Integer, default=15)
    player_id   = Column(Integer, ForeignKey('players.id'), nullable=False)
    player      = relationship("Player", foreign_keys=[player_id])


class Item(Base):
    __tablename__ = 'items'

    id              = Column(Integer, primary_key=True)
    item_type       = Column(String)
    lifeform_id     = Column(Integer, ForeignKey('lifeforms.id'))
    lifeform        = relationship("Lifeform", foreign_keys=[lifeform_id])
    material_type   = Column(String)
    modifiers       = relationship("Modifier", cascade="all, delete-orphan")
    item_attributes = Column(JSON, nullable=True)


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
    lifeform_id     = Column(Integer, ForeignKey('lifeforms.id'))
    lifeform        = relationship("Lifeform", foreign_keys=[lifeform_id])

