from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from erukar.data.SchemaBase import Base

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
    instance    = Column(String)
    health      = Column(Integer, default=4)
    strength    = Column(Integer, default=0)
    dexterity   = Column(Integer, default=0)
    vitality    = Column(Integer, default=0)
    acuity      = Column(Integer, default=0)
    sense       = Column(Integer, default=0)
    resolve     = Column(Integer, default=0)

    wealth      = Column(Integer, default=0)
    level       = Column(Integer, default=1)
    experience  = Column(Integer, default=0)

    skills      = relationship("Skill", cascade="all, delete-orphan") 
    spell_words = relationship("SpellWord", cascade="all, delete-orphan")
    equipment   = relationship("EquippedItem", cascade="all, delete-orphan")
    inventory   = relationship("Item", cascade="all, delete-orphan")
    effects     = relationship("Effect", cascade="all, delete-orphan")
